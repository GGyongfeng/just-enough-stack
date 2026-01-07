"""
标准响应模型
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class StandardResponse(BaseModel):
    """标准 API 响应模型

    使用此模型可确保所有 API 端点返回统一格式的响应

    Attributes:
        success: 请求是否成功
        message: 响应消息
        data: 响应数据（可选）

    Examples:
        >>> # 成功响应
        >>> response = StandardResponse(
        ...     success=True,
        ...     message="操作成功",
        ...     data={"id": 123, "name": "John"}
        ... )
        >>>
        >>> # 失败响应
        >>> response = StandardResponse(
        ...     success=False,
        ...     message="操作失败：权限不足"
        ... )
    """

    success: bool = Field(..., description="请求是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[Dict[str, Any]] = Field(None, description="响应数据")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "success": True,
                    "message": "操作成功",
                    "data": {"id": 1, "username": "john"},
                },
                {"success": False, "message": "操作失败：未找到资源"},
            ]
        }


def success_response(message: str, data: Optional[Dict[str, Any]] = None) -> StandardResponse:
    """创建成功响应

    Args:
        message: 成功消息
        data: 响应数据

    Returns:
        StandardResponse 对象

    Example:
        >>> return success_response("创建成功", {"id": 123})
    """
    return StandardResponse(success=True, message=message, data=data)


def error_response(message: str, data: Optional[Dict[str, Any]] = None) -> StandardResponse:
    """创建错误响应

    Args:
        message: 错误消息
        data: 额外的错误数据

    Returns:
        StandardResponse 对象

    Example:
        >>> return error_response("创建失败：用户名已存在")
    """
    return StandardResponse(success=False, message=message, data=data)
