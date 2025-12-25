from pydantic import BaseModel
from typing import Optional


class UserLoginRequest(BaseModel):
    """用户登录请求模型"""

    username: str
    password: str


class UserResponse(BaseModel):
    """用户响应模型"""

    id: int
    username: str
    nickname: str
    full_name: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None


class LoginResponse(BaseModel):
    """登录响应模型"""

    access_token: str
    token_type: str = "bearer"
    expires_in_days: int = 15
    user: UserResponse
