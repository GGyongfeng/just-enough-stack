from loguru import logger
from sqlalchemy.orm import Session

from src.orm import UserModel
from src.exc import AlreadyExistsError, NotExistsError
from src.types.user_role import UserRole

from .base import BaseDAO


class UserDAO(BaseDAO):
    """用户表单管理器 - SQLAlchemy版本"""

    def __init__(self, session: Session):
        super().__init__(session, UserModel)

    def add_user(
        self,
        username: str,
        password: str,
        nickname: str,
        full_name: str | None = None,
        role: str = UserRole.GUEST,
        is_active: bool = True,
    ):
        """添加用户 - 使用ORM方式，新用户默认为游客权限"""

        # 检查用户名是否已存在
        existing_user = (
            self._session.query(UserModel).filter_by(username=username).one_or_none()
        )
        if existing_user:
            logger.info(f"✗ 用户名 '{username}' 已存在")
            raise AlreadyExistsError()

        # 创建新用户
        new_user = UserModel(
            username=username,
            password=password,
            nickname=nickname,
            full_name=full_name,
            role=role,
            is_active=is_active,
        )

        self._session.add(new_user)
        self._session.commit()

        logger.info(f"✓ 用户 '{username}' 添加成功！角色: {UserRole.get_description(role)}")

    def get_user_by_username(self, username: str) -> UserModel | None:
        """根据用户名获取用户"""

        user = self._session.query(UserModel).filter_by(username=username).one_or_none()

        return user

    def get_user_info_by_id(self, user_id: int) -> dict | None:
        """
        根据用户ID获取用户信息

        Args:
            user_id: 用户ID

        Returns:
            dict: 包含nickname, full_name, username的字典，如果用户不存在返回None
        """
        try:
            user = self.get_line_by_id(user_id)
            if not user:
                return None

            return {
                "nickname": user.nickname,
                "full_name": user.full_name,
                "username": user.username,
            }
        except Exception as e:
            logger.error(f"获取用户信息时发生错误: {str(e)}")
            return None

    def update_user(self, username: str, **kwargs):
        """更新用户信息"""

        user = self._session.query(UserModel).filter_by(username=username).one_or_none()

        if not user:
            logger.info(f"✗ 用户 '{username}' 不存在")
            raise NotExistsError()

        # 更新字段
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self._session.commit()
        logger.info(f"✓ 用户 '{username}' 更新成功！")

    def delete_user(self, username: str):
        """删除用户"""

        user = self._session.query(UserModel).filter_by(username=username).one_or_none()

        if not user:
            logger.info(f"✗ 用户 '{username}' 不存在")
            raise NotExistsError()

        self._session.delete(user)
        self._session.commit()

        logger.info(f"✓ 用户 '{username}' 删除成功！")

    def get_all_users(self) -> list[UserModel]:
        """获取所有用户列表"""
        return self._session.query(UserModel).all()

    def get_users_with_pagination(self, page: int = 1, per_page: int = 20) -> dict:
        """分页获取用户列表"""
        offset = (page - 1) * per_page
        users = self._session.query(UserModel).offset(offset).limit(per_page).all()
        total = self._session.query(UserModel).count()

        return {
            "users": users,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page
        }

    def update_user_role(self, user_id: int, role: str) -> bool:
        """更新用户权限"""
        if role not in [r.value for r in UserRole]:
            logger.error(f"无效的角色: {role}")
            return False

        user = self.get_line_by_id(user_id)
        if not user:
            logger.error(f"用户不存在: ID {user_id}")
            return False

        old_role = user.role
        user.role = role
        self._session.commit()

        logger.info(f"✓ 用户 '{user.username}' 权限更新成功！{old_role} -> {role}")
        return True

    def update_user_status(self, user_id: int, is_active: bool) -> bool:
        """更新用户激活状态"""
        user = self.get_line_by_id(user_id)
        if not user:
            logger.error(f"用户不存在: ID {user_id}")
            return False

        old_status = user.is_active
        user.is_active = is_active
        self._session.commit()

        status_text = "激活" if is_active else "禁用"
        logger.info(f"✓ 用户 '{user.username}' 状态更新成功！{old_status} -> {status_text}")
        return True

    def search_users(self, keyword: str) -> list[UserModel]:
        """搜索用户"""
        return self._session.query(UserModel).filter(
            UserModel.username.contains(keyword) |
            UserModel.nickname.contains(keyword) |
            UserModel.full_name.contains(keyword)
        ).all()

    def get_users_by_role(self, role: str) -> list[UserModel]:
        """根据角色获取用户列表"""
        return self._session.query(UserModel).filter_by(role=role).all()
