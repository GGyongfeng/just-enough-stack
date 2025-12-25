"""
用户权限角色定义
"""

from enum import Enum


class UserRole(str, Enum):
    """用户角色枚举"""

    GUEST = "guest"         # 游客 - 只能查看
    USER = "user"           # 普通用户 - 可以创建查询和评估
    ADMIN = "admin"         # 管理员 - 可以管理用户和系统设置
    SUPER_ADMIN = "super_admin"  # 超级管理员 - 所有权限

    @classmethod
    def get_description(cls, role: str) -> str:
        """获取角色描述"""
        descriptions = {
            cls.GUEST: "游客 - 只能查看公开内容",
            cls.USER: "普通用户 - 可以创建和管理自己的查询和评估",
            cls.ADMIN: "管理员 - 可以管理用户权限和系统设置",
            cls.SUPER_ADMIN: "超级管理员 - 拥有所有权限"
        }
        return descriptions.get(role, "未知角色")

    @classmethod
    def get_permissions(cls, role: str) -> list[str]:
        """获取角色权限列表"""
        permissions = {
            cls.GUEST: [
                "view_public_queries",
                "view_public_evaluations"
            ],
            cls.USER: [
                "view_public_queries",
                "view_public_evaluations",
                "create_query",
                "edit_own_query",
                "delete_own_query",
                "create_evaluation",
                "edit_own_evaluation",
                "delete_own_evaluation",
                "upload_deliverables"
            ],
            cls.ADMIN: [
                "view_public_queries",
                "view_public_evaluations",
                "create_query",
                "edit_own_query",
                "delete_own_query",
                "edit_any_query",
                "delete_any_query",
                "create_evaluation",
                "edit_own_evaluation",
                "delete_own_evaluation",
                "edit_any_evaluation",
                "delete_any_evaluation",
                "upload_deliverables",
                "manage_users",
                "view_user_list",
                "edit_user_permissions"
            ],
            cls.SUPER_ADMIN: [
                "*"  # 所有权限
            ]
        }
        return permissions.get(role, [])

    @classmethod
    def can_access(cls, user_role: str, required_permission: str) -> bool:
        """检查用户角色是否有指定权限"""
        if user_role == cls.SUPER_ADMIN:
            return True

        user_permissions = cls.get_permissions(user_role)
        return required_permission in user_permissions or "*" in user_permissions

    @classmethod
    def get_all_roles(cls) -> list[dict]:
        """获取所有角色信息"""
        return [
            {
                "value": role.value,
                "label": cls.get_description(role.value),
                "permissions": cls.get_permissions(role.value)
            }
            for role in cls
        ]