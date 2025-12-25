"""
抽象基类 - 表单管理基类

所有表单管理类都应该继承这个基类
使用SQLAlchemy重写，逻辑不变
"""

from abc import ABC
from typing import Type

from loguru import logger
from sqlalchemy.orm import Session, DeclarativeMeta


class FormValidationError(Exception):
    """表单验证错误"""

    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class BaseDAO(ABC):
    def __init__(self, session: Session, Model: Type[DeclarativeMeta]):
        self._session = session
        self.name = Model.__name__
        self.Model = Model

    def add_line(self, **line_data):
        """添加数据行"""
        # 创建模型实例
        new_line = self.Model(**line_data)
        # 添加到会话
        self._session.add(new_line)
        # 提交事务
        self._session.commit()
        logger.info(f"{self.name}添加成功,ID: {new_line.id}")

    def get_liness_num(self):
        """获取数据行数量"""
        return self._session.query(self.Model).count()

    def get_lines(self) -> list:
        return self._session.query(self.Model).all()

    def get_line_by_id(self, id: int):
        """根据ID获取单条数据"""
        return self._session.query(self.Model).filter(self.Model.id == id).first()
