import asyncio
import os
from typing import Dict, Any, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger

from src.middleware.auth import (
    CurrentUser,
    check_user_permission,
    create_token_for_user,
    hash_password,
    verify_password,
)
from src.dao.user_dao import UserDAO
from src.types.standard_response import StandardResponse
from src.types.models import UserType
from src.types.users import UserLoginRequest, UserResponse, LoginResponse

from ..utils import exception_wrapper, get_db_session

# 创建用户路由 - 路径对应 /user
router = APIRouter(prefix="/user", tags=["用户管理"])


class AuthService:
    """用户认证服务"""

    def __init__(self, session: Session):
        self.user_dao = UserDAO(session)

    def register_user(self, user_data: UserType) -> UserResponse:
        """用户注册"""
        try:
            existing_user = self.user_dao.get_user_by_username(user_data.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"用户名 '{user_data.username}' 已存在",
                )
            if len(user_data.username) < 3:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名长度至少为3个字符",
                )
            if len(user_data.password) < 6:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="密码长度至少为6个字符",
                )
            hashed_password = hash_password(user_data.password)
            self.user_dao.add_user(
                username=user_data.username,
                password=hashed_password,
                nickname=user_data.nickname,
                full_name=user_data.full_name,
            )
            new_user = self.user_dao.get_user_by_username(user_data.username)
            if not new_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="无法获取新创建的用户信息",
                )
            logger.info(f"✓ 用户 '{user_data.username}' 注册成功！")
            return UserResponse(
                id=new_user.id,
                username=new_user.username,
                nickname=new_user.nickname,
                full_name=new_user.full_name,
                updated_at=new_user.updated_at.isoformat(),
                created_at=new_user.created_at.isoformat(),
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"✗ 用户注册异常: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="用户注册过程中发生错误",
            )

    def login_user(self, login_data: UserLoginRequest) -> LoginResponse:
        """用户登录"""
        try:
            user = self.user_dao.get_user_by_username(login_data.username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
                )
            if not verify_password(login_data.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
                )
            access_token = create_token_for_user(
                username=user.username,
                user_id=user.id,
                nickname=user.nickname,
                role=user.role,
                is_active=user.is_active,
                full_name=user.full_name,
            )
            logger.info(f"✓ 用户 '{login_data.username}' 登录成功！")
            return LoginResponse(
                access_token=access_token,
                user=UserResponse(
                    id=user.id,
                    username=user.username,
                    nickname=user.nickname,
                    full_name=user.full_name,
                    created_at=user.created_at.isoformat(),
                    updated_at=user.updated_at.isoformat(),
                ),
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"✗ 用户登录异常: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="用户登录过程中发生错误",
            )

    def get_user_profile(self, username: str) -> UserResponse:
        """获取用户信息"""
        try:
            user = self.user_dao.get_user_by_username(username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
                )
            return UserResponse(
                id=user.id,
                username=user.username,
                nickname=user.nickname,
                full_name=user.full_name,
                created_at=user.created_at.isoformat(),
                updated_at=user.updated_at.isoformat(),
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"✗ 获取用户信息异常: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="获取用户信息过程中发生错误",
            )

    def update_user_profile(
        self, username: str, update_data: Dict[str, Any]
    ) -> UserResponse:
        """更新用户信息"""
        try:
            user = self.user_dao.get_user_by_username(username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
                )
            allowed_fields = ["nickname", "full_name"]
            filtered_data = {
                k: v for k, v in update_data.items() if k in allowed_fields
            }
            if not filtered_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="没有提供有效的更新字段",
                )
            self.user_dao.update_user(username, **filtered_data)
            updated_user = self.user_dao.get_user_by_username(username)
            assert updated_user, f"User not found where username={username}"
            return UserResponse(
                id=updated_user.id,
                username=updated_user.username,
                nickname=updated_user.nickname,
                full_name=updated_user.full_name,
                created_at=updated_user.created_at.isoformat(),
                updated_at=updated_user.updated_at.isoformat(),
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"✗ 更新用户信息异常: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="更新用户信息过程中发生错误",
            )


def get_auth_service(db_session: Annotated[Session, Depends(get_db_session)]):
    return AuthService(db_session)


@router.post(
    "/register", response_model=StandardResponse, status_code=status.HTTP_201_CREATED
)
@exception_wrapper(catch_http_exc=True)
async def register_user(
    user_data: UserType,
    auth_service: AuthService = Depends(get_auth_service),
):
    """用户注册 - POST /user/register"""
    token = os.getenv("USER_REGISTER_TOKEN", None)
    if token is None:
        raise HTTPException(status_code=501, detail="服务器未设置注册 Token")
    if user_data.register_token != token:
        await asyncio.sleep(3.0)
        raise HTTPException(status_code=403, detail="错误的注册 Token")

    user = auth_service.register_user(user_data)
    return StandardResponse(
        success=True,
        message="用户注册成功",
        data={
            "user": {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "full_name": user.full_name,
                "created_at": user.created_at,
            },
        },
    )


@router.post("/login", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def login_user(
    login_data: UserLoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """用户登录 - POST /user/login"""
    login_response = auth_service.login_user(login_data)
    return StandardResponse(
        success=True,
        message="登录成功",
        data={
            "access_token": login_response.access_token,
            "token_type": login_response.token_type,
            "expires_in_days": login_response.expires_in_days,
            "user": {
                "id": login_response.user.id,
                "username": login_response.user.username,
                "nickname": login_response.user.nickname,
                "full_name": login_response.user.full_name,
                "created_at": login_response.user.created_at,
            },
        },
    )


@router.get("/profile", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def get_current_user_profile(
    current_user: CurrentUser = Depends(check_user_permission()),
    auth_service: AuthService = Depends(get_auth_service),
):
    """获取当前用户信息 - GET /user/profile"""
    username = current_user.username
    user = auth_service.get_user_profile(username)
    return StandardResponse(
        success=True,
        message="获取用户信息成功",
        data={
            "user": {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "full_name": user.full_name,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            },
        },
    )


@router.put("/profile", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def update_current_user_profile(
    update_data: UserType,
    current_user: CurrentUser = Depends(check_user_permission()),
    auth_service: AuthService = Depends(get_auth_service),
):
    """更新当前用户信息 - PUT /user/profile"""
    username = current_user.username

    # 过滤非空字段
    update_dict = {}
    if update_data.nickname is not None:
        update_dict["nickname"] = update_data.nickname
    if update_data.full_name is not None:
        update_dict["full_name"] = update_data.full_name

    if not update_dict:
        return StandardResponse(
            success=False, message="没有提供要更新的字段", data={"error_code": 400}
        )

    user = auth_service.update_user_profile(username, update_dict)
    return StandardResponse(
        success=True,
        message="用户信息更新成功",
        data={
            "user": {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "full_name": user.full_name,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            },
        },
    )
