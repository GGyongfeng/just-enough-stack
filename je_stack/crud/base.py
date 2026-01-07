"""
抽象基类 - 数据访问对象基类

所有 DAO 类都应该继承这个基类，提供统一的数据访问接口
"""

from abc import ABC
from typing import Type, TypeVar, Generic, Optional, List, Any, Dict
from sqlalchemy.orm import Session, DeclarativeMeta
from loguru import logger

# 泛型类型变量
T = TypeVar("T", bound=DeclarativeMeta)


class FormValidationError(Exception):
    """表单验证错误

    当数据验证失败时抛出此异常

    Attributes:
        message: 错误消息
        error_code: 错误代码
    """

    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class BaseDAO(ABC, Generic[T]):
    """数据访问对象基类

    提供基本的 CRUD 操作，所有 DAO 类都应该继承此基类

    Attributes:
        _session: SQLAlchemy Session
        Model: SQLAlchemy ORM 模型类
        name: 模型名称

    Examples:
        >>> from sqlalchemy.orm import Session
        >>> from your_models import UserModel
        >>>
        >>> class UserDAO(BaseDAO[UserModel]):
        ...     def get_by_username(self, username: str):
        ...         return self._session.query(self.Model).filter(
        ...             self.Model.username == username
        ...         ).first()
        >>>
        >>> # 使用
        >>> session = Session()
        >>> user_dao = UserDAO(session, UserModel)
        >>> user_dao.add_line(username="john", password="hashed")
    """

    def __init__(self, session: Session, Model: Type[T]):
        """初始化 DAO

        Args:
            session: SQLAlchemy Session 实例
            Model: SQLAlchemy ORM 模型类
        """
        self._session = session
        self.name = Model.__name__
        self.Model = Model

    def add_line(self, **line_data: Any) -> T:
        """添加数据行

        Args:
            **line_data: 数据字段键值对

        Returns:
            创建的模型实例

        Raises:
            FormValidationError: 数据验证失败

        Example:
            >>> user = dao.add_line(username="john", email="john@example.com")
            >>> print(user.id)
        """
        # 创建模型实例
        new_line = self.Model(**line_data)  # type: ignore
        # 添加到会话
        self._session.add(new_line)
        # 提交事务
        self._session.commit()
        # 刷新实例以获取生成的字段（如 ID）
        self._session.refresh(new_line)
        logger.info(f"{self.name}添加成功, ID: {new_line.id}")  # type: ignore
        return new_line

    def get_lines_num(self) -> int:
        """获取数据行数量

        Returns:
            数据行总数

        Example:
            >>> count = dao.get_lines_num()
            >>> print(f"Total records: {count}")
        """
        return self._session.query(self.Model).count()

    def get_lines(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[T]:
        """获取所有数据行（支持分页）

        Args:
            limit: 限制返回数量
            offset: 跳过前 N 条记录

        Returns:
            数据行列表

        Example:
            >>> # 获取所有记录
            >>> all_users = dao.get_lines()
            >>>
            >>> # 分页获取（第2页，每页10条）
            >>> users_page2 = dao.get_lines(limit=10, offset=10)
        """
        query = self._session.query(self.Model)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def get_line_by_id(self, id: int) -> Optional[T]:
        """根据 ID 获取单条数据

        Args:
            id: 记录 ID

        Returns:
            模型实例，如果不存在返回 None

        Example:
            >>> user = dao.get_line_by_id(123)
            >>> if user:
            ...     print(user.username)
        """
        return self._session.query(self.Model).filter(self.Model.id == id).first()  # type: ignore

    def update_line(self, id: int, **update_data: Any) -> Optional[T]:
        """更新数据行

        Args:
            id: 记录 ID
            **update_data: 要更新的字段键值对

        Returns:
            更新后的模型实例，如果记录不存在返回 None

        Example:
            >>> updated_user = dao.update_line(123, email="newemail@example.com")
            >>> if updated_user:
            ...     print("Updated successfully")
        """
        line = self.get_line_by_id(id)
        if not line:
            return None

        # 更新字段
        for key, value in update_data.items():
            if hasattr(line, key):
                setattr(line, key, value)

        self._session.commit()
        self._session.refresh(line)
        logger.info(f"{self.name} ID={id} 更新成功")
        return line

    def delete_line(self, id: int) -> bool:
        """删除数据行

        Args:
            id: 记录 ID

        Returns:
            是否删除成功

        Example:
            >>> success = dao.delete_line(123)
            >>> if success:
            ...     print("Deleted successfully")
        """
        line = self.get_line_by_id(id)
        if not line:
            return False

        self._session.delete(line)
        self._session.commit()
        logger.info(f"{self.name} ID={id} 删除成功")
        return True

    def get_lines_by_field(
        self, field_name: str, value: Any, limit: Optional[int] = None
    ) -> List[T]:
        """根据字段值查询数据

        Args:
            field_name: 字段名
            value: 字段值
            limit: 限制返回数量

        Returns:
            匹配的数据行列表

        Example:
            >>> users = dao.get_lines_by_field("role", "admin")
            >>> for user in users:
            ...     print(user.username)
        """
        query = self._session.query(self.Model).filter(
            getattr(self.Model, field_name) == value
        )

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def exists(self, id: int) -> bool:
        """检查记录是否存在

        Args:
            id: 记录 ID

        Returns:
            记录是否存在

        Example:
            >>> if dao.exists(123):
            ...     print("Record exists")
        """
        return (
            self._session.query(self.Model).filter(self.Model.id == id).count() > 0  # type: ignore
        )

    def count_by_field(self, field_name: str, value: Any) -> int:
        """统计符合条件的记录数

        Args:
            field_name: 字段名
            value: 字段值

        Returns:
            记录数量

        Example:
            >>> active_count = dao.count_by_field("is_active", True)
        """
        return (
            self._session.query(self.Model)
            .filter(getattr(self.Model, field_name) == value)
            .count()
        )
