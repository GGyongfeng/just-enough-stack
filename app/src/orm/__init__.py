from datetime import datetime

from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Float, BLOB
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase

from src.types.user_role import UserRole


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    """用户表单ORM模型"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="用户ID",
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="用户名",
    )
    password: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="密码",
    )
    nickname: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="昵称",
    )
    full_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="全名",
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        default=UserRole.GUEST,
        comment="用户角色：guest/user/admin/super_admin",
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=True,
        default=True,
        comment="用户是否激活",
    )
    extra: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="额外信息",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="创建时间",
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        comment="更新时间",
        default=datetime.now,
        onupdate=datetime.now,
    )

    # 关系定义
    tasks: Mapped[list["TaskModel"]] = relationship(
        "TaskModel",
        back_populates="creator",
    )

    def __repr__(self):
        return f"<UserModel(id={self.id}, username='{self.username}', nickname='{self.nickname}', role='{self.role}')>"

    def has_permission(self, permission: str) -> bool:
        """检查用户是否有指定权限"""
        if not self.is_active:
            return False
        return UserRole.can_access(self.role, permission)

    def is_admin(self) -> bool:
        """检查是否为管理员"""
        return self.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]

    def is_super_admin(self) -> bool:
        """检查是否为超级管理员"""
        return self.role == UserRole.SUPER_ADMIN

    def get_role_description(self) -> str:
        """获取角色描述"""
        return UserRole.get_description(self.role)

    def get_permissions(self) -> list[str]:
        """获取用户权限列表"""
        if not self.is_active:
            return []
        return UserRole.get_permissions(self.role)


class TaskModel(Base):
    """任务表单ORM模型"""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="任务ID",
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="任务标题",
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="任务描述",
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        comment="状态: pending/in_progress/completed/cancelled",
    )
    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        comment="优先级: low/medium/high",
    )
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="截止日期",
    )
    creator_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        comment="创建人ID",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        comment="创建时间",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间",
    )

    # 关系定义
    creator: Mapped[UserModel | None] = relationship(
        "UserModel",
        back_populates="tasks",
    )

    def __repr__(self):
        return f"<TaskModel(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority}')>"
