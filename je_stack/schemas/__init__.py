"""
Pydantic Schemas - 单一事实源（SSOT）
"""

from .user_role import UserRole
from .response import StandardResponse

__all__ = [
    "UserRole",
    "StandardResponse",
]
