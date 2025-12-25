"""
用户管理 API 路由
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from loguru import logger
from pydantic import BaseModel, Field

from src.middleware.auth import CurrentUser, check_user_permission
from src.dao.user_dao import UserDAO
from src.types.standard_response import StandardResponse
from src.types.user_role import UserRole
from ..utils import exception_wrapper, get_db_session


class UserManagementResponse(BaseModel):
    """用户管理响应模型"""

    id: int
    username: str
    nickname: str
    full_name: Optional[str] = None
    role: str
    role_description: str
    is_active: bool
    created_at: str
    updated_at: str
    permissions: list[str]


class UserRoleUpdateRequest(BaseModel):
    """用户角色更新请求模型"""

    user_id: int = Field(..., description="用户ID")
    role: str = Field(
        ...,
        description="新角色",
        pattern=f"^({'|'.join([r.value for r in UserRole])})$",
    )


class UserStatusUpdateRequest(BaseModel):
    """用户状态更新请求模型"""

    user_id: int = Field(..., description="用户ID")
    is_active: bool = Field(..., description="是否激活")


class UserListQuery(BaseModel):
    """用户列表查询参数"""

    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页条数")
    role: Optional[str] = Field(None, description="按角色筛选")
    keyword: Optional[str] = Field(None, description="搜索关键词")
    is_active: Optional[bool] = Field(None, description="按状态筛选")


class RoleInfo(BaseModel):
    """角色信息"""

    value: str
    label: str
    permissions: list[str]


class UserPermissionsResponse(BaseModel):
    """用户权限响应"""

    user_id: int
    username: str
    role: str
    permissions: list[str]
    can_manage_users: bool
    is_admin: bool
    is_super_admin: bool


class UsersListResponse(BaseModel):
    """用户列表响应"""

    users: list[UserManagementResponse]
    total: int
    page: int
    per_page: int
    pages: int


# 创建用户管理路由
router = APIRouter(prefix="/user-management", tags=["用户管理"])


@router.get("/users", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def get_users_list(
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(20, ge=1, le=100, description="每页条数"),
    role: Optional[str] = Query(None, description="按角色筛选"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    is_active: Optional[bool] = Query(None, description="按状态筛选"),
    current_user: CurrentUser = Depends(check_user_permission()),
    db_session: Session = Depends(get_db_session),
):
    """获取用户列表.

    Args:
        page (int): 页码，默认为1
        per_page (int): 每页条数，默认为20，最大100
        role (Optional[str]): 按角色筛选，可选
        keyword (Optional[str]): 搜索关键词，可选
        is_active (Optional[bool]): 按状态筛选，可选
        current_user (CurrentUser): 当前登录用户信息
        db_session (Session): 数据库会话

    Returns:
        StandardResponse: 包含用户列表数据的标准响应
    """
    try:
        user_dao = UserDAO(db_session)

        # 根据查询条件获取用户
        if keyword:
            users = user_dao.search_users(keyword)
            total = len(users)
            # 简单分页处理
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            users = users[start_idx:end_idx]
        elif role:
            users = user_dao.get_users_by_role(role)
            total = len(users)
            # 简单分页处理
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            users = users[start_idx:end_idx]
        else:
            result = user_dao.get_users_with_pagination(page, per_page)
            users = result["users"]
            total = result["total"]

        # 状态筛选
        if is_active is not None:
            users = [u for u in users if u.is_active == is_active]

        # 转换为响应格式
        user_responses = []
        for user in users:
            user_responses.append(
                UserManagementResponse(
                    id=user.id,
                    username=user.username,
                    nickname=user.nickname,
                    full_name=user.full_name,
                    role=user.role,
                    role_description=user.get_role_description(),
                    is_active=user.is_active,
                    created_at=user.created_at.isoformat(),
                    updated_at=user.updated_at.isoformat() if user.updated_at else "",
                    permissions=user.get_permissions(),
                )
            )

        pages = (total + per_page - 1) // per_page

        result = UsersListResponse(
            users=user_responses,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        )

        return StandardResponse(
            success=True, message="获取用户列表成功", data=result.model_dump()
        )

    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户列表失败",
        )


@router.put("/users/role", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def update_user_role(
    request: UserRoleUpdateRequest,
    current_user: CurrentUser = Depends(check_user_permission()),
    db_session: Session = Depends(get_db_session),
):
    """更新用户角色.

    Args:
        request (UserRoleUpdateRequest): 用户角色更新请求数据
        current_user (CurrentUser): 当前登录用户信息
        db_session (Session): 数据库会话

    Returns:
        StandardResponse: 包含更新后用户信息的标准响应
    """
    try:
        user_dao = UserDAO(db_session)

        success = user_dao.update_user_role(request.user_id, request.role)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在或角色无效"
            )

        # 获取更新后的用户信息
        user = user_dao.get_line_by_id(request.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
            )

        result = UserManagementResponse(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            full_name=user.full_name,
            role=user.role,
            role_description=user.get_role_description(),
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat() if user.updated_at else "",
            permissions=user.get_permissions(),
        )

        return StandardResponse(
            success=True, message="用户角色更新成功", data={"user": result.model_dump()}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新用户角色失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户角色失败",
        )


@router.put("/users/status", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def update_user_status(
    request: UserStatusUpdateRequest,
    current_user: CurrentUser = Depends(check_user_permission()),
    db_session: Session = Depends(get_db_session),
):
    """更新用户状态.

    Args:
        request (UserStatusUpdateRequest): 用户状态更新请求数据
        current_user (CurrentUser): 当前登录用户信息
        db_session (Session): 数据库会话

    Returns:
        StandardResponse: 包含更新后用户信息的标准响应
    """
    try:
        user_dao = UserDAO(db_session)

        success = user_dao.update_user_status(request.user_id, request.is_active)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
            )

        # 获取更新后的用户信息
        user = user_dao.get_line_by_id(request.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
            )

        result = UserManagementResponse(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            full_name=user.full_name,
            role=user.role,
            role_description=user.get_role_description(),
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat() if user.updated_at else "",
            permissions=user.get_permissions(),
        )

        return StandardResponse(
            success=True, message="用户状态更新成功", data={"user": result.model_dump()}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新用户状态失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户状态失败",
        )


@router.get("/users/{user_id}/permissions", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def get_user_permissions(
    user_id: int,
    current_user: CurrentUser = Depends(check_user_permission()),
    db_session: Session = Depends(get_db_session),
):
    """获取用户权限信息.

    Args:
        user_id (int): 用户ID
        current_user (CurrentUser): 当前登录用户信息
        db_session (Session): 数据库会话

    Returns:
        StandardResponse: 包含用户权限信息的标准响应
    """
    try:
        user_dao = UserDAO(db_session)

        user = user_dao.get_line_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
            )

        result = UserPermissionsResponse(
            user_id=user.id,
            username=user.username,
            role=user.role,
            permissions=user.get_permissions(),
            can_manage_users=user.has_permission("manage_users"),
            is_admin=user.is_admin(),
            is_super_admin=user.is_super_admin(),
        )

        return StandardResponse(
            success=True, message="获取用户权限成功", data=result.model_dump()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户权限失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户权限失败",
        )


@router.get("/current-permissions", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def get_current_user_permissions(
    current_user: CurrentUser = Depends(check_user_permission()),
    db_session: Session = Depends(get_db_session),
):
    """获取当前用户权限信息.

    Args:
        current_user (CurrentUser): 当前登录用户信息
        db_session (Session): 数据库会话

    Returns:
        StandardResponse: 包含当前用户权限信息的标准响应
    """
    try:
        user_dao = UserDAO(db_session)

        user = user_dao.get_user_by_username(current_user.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
            )

        result = UserPermissionsResponse(
            user_id=user.id,
            username=user.username,
            role=user.role,
            permissions=user.get_permissions(),
            can_manage_users=user.has_permission("manage_users"),
            is_admin=user.is_admin(),
            is_super_admin=user.is_super_admin(),
        )

        return StandardResponse(
            success=True, message="获取当前用户权限成功", data=result.model_dump()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取当前用户权限失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取当前用户权限失败",
        )
