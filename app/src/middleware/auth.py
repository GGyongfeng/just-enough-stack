import os
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Callable
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pydantic import BaseModel

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 15

# HTTP Bearer认证
security = HTTPBearer()


class CurrentUser(BaseModel):
    username: str
    user_id: int
    nickname: Optional[str] = None
    role: Optional[str] = None
    is_active: bool = True
    full_name: Optional[str] = None
    exp: datetime


class AuthMiddlewareTool:
    """JWT认证中间件"""

    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                days=ACCESS_TOKEN_EXPIRE_DAYS
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        """验证令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token已过期",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的Token格式",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的Token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """获取密码哈希"""
        return pwd_context.hash(password)

    def get_current_user(
        self, credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> CurrentUser:
        """获取当前用户信息"""
        token = credentials.credentials
        payload = self.verify_token(token)

        username = payload.get("sub")
        if not isinstance(username, str) or not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的Token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return CurrentUser(
            username=username,
            user_id=payload.get("user_id"),  # type: ignore
            nickname=payload.get("nickname"),
            role=payload.get("role"),
            is_active=payload.get("is_active", True),
            full_name=payload.get("full_name"),
            exp=payload.get("exp"),  # type: ignore
        )


# 创建全局认证中间件实例
auth_middleware = AuthMiddlewareTool()


def create_token_for_user(
    username: str,
    user_id: int,
    nickname: str = None,
    role: str = None,
    is_active: bool = True,
    full_name: str = None,
) -> str:
    """为用户创建令牌，包含更多用户信息"""
    token_data = {
        "sub": username,
        "user_id": user_id,
        "nickname": nickname,
        "role": role,
        "is_active": is_active,
        "full_name": full_name,
    }
    # 移除 None 值，减少 token 大小
    token_data = {k: v for k, v in token_data.items() if v is not None}

    return auth_middleware.create_access_token(data=token_data)


def hash_password(password: str) -> str:
    """哈希密码"""
    return auth_middleware.get_password_hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return auth_middleware.verify_password(plain_password, hashed_password)


def check_user_permission(
    permission: Optional[str] = None, role: Optional[str] = None
) -> Callable:
    """统一的权限检查依赖函数

    Args:
        permission: 需要的权限字符串，如 'create_query', 'manage_users' 等
        role: 需要的角色，如 'admin', 'super_admin' 等

    当 permission 和 role 都为 None 时，只检查用户是否存在和激活
    当 permission 不为 None 时，检查用户是否有指定权限
    当 role 不为 None 时，检查用户是否有指定角色
    不能同时指定 permission 和 role

    Returns:
        依赖函数，可以在 FastAPI 路由中使用

    Examples:
        # 只检查用户登录
        @router.get("/profile")
        def get_profile(
            current_user: CurrentUser = Depends(check_user_permission())
        ):
            pass

        # 检查权限
        @router.post("/queries")
        def create_query(
            current_user: CurrentUser = Depends(check_user_permission(permission="create_query"))
        ):
            pass

        # 检查角色
        @router.delete("/users/{user_id}")
        def delete_user(
            current_user: CurrentUser = Depends(check_user_permission(role="admin"))
        ):
            pass
    """
    if permission is not None and role is not None:
        raise ValueError("不能同时指定 permission 和 role")

    def auth_checker(
        current_user: CurrentUser = Depends(auth_middleware.get_current_user),
    ) -> CurrentUser:
        """统一的权限检查器"""
        from src.types.user_role import UserRole

        # 检查用户是否激活
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="账户已被禁用"
            )

        # 如果没有指定权限和角色，放行
        if permission is None and role is None:
            return current_user

        # 超级管理员拥有所有权限，放行
        if current_user.role == UserRole.SUPER_ADMIN:
            return current_user

        # 有权限要求，检查权限
        if permission is not None:
            if not UserRole.can_access(current_user.role or "guest", permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"权限不足，需要权限: {permission}",
                )

        # 有角色要求，检查角色
        if role is not None:
            if current_user.role != role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"权限不足，需要角色: {role}",
                )

        return current_user

    return auth_checker
