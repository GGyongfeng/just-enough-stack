"""任务管理 API 端点"""

from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger

from src.middleware.auth import CurrentUser, check_user_permission
from src.dao.task_dao import TaskDAO
from src.types.standard_response import StandardResponse
from src.types.task_models import TaskCreate, TaskUpdate, TaskResponse
from ..utils import exception_wrapper, get_db_session

router = APIRouter(prefix="/tasks", tags=["任务管理"])


def get_task_dao(db_session: Annotated[Session, Depends(get_db_session)]):
    """获取任务 DAO 依赖"""
    return TaskDAO(db_session)


@router.post("/", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
@exception_wrapper(catch_http_exc=True)
async def create_task(
    task_data: TaskCreate,
    current_user: CurrentUser = Depends(check_user_permission()),
    task_dao: TaskDAO = Depends(get_task_dao),
):
    """创建任务"""
    task = task_dao.create_task(
        title=task_data.title,
        creator_id=current_user.user_id,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
    )

    return StandardResponse(
        success=True, message="任务创建成功", data={"task": TaskResponse.from_orm(task).dict()}
    )


@router.get("/", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: CurrentUser = Depends(check_user_permission()),
    task_dao: TaskDAO = Depends(get_task_dao),
):
    """获取任务列表（分页）"""
    tasks = task_dao.get_all_tasks(skip=skip, limit=limit)

    return StandardResponse(
        success=True,
        message="获取任务列表成功",
        data={
            "tasks": [TaskResponse.from_orm(t).dict() for t in tasks],
            "total": len(tasks),
            "skip": skip,
            "limit": limit,
        },
    )


@router.get("/my", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def get_my_tasks(
    current_user: CurrentUser = Depends(check_user_permission()),
    task_dao: TaskDAO = Depends(get_task_dao),
):
    """获取我的任务"""
    tasks = task_dao.get_tasks_by_creator(current_user.user_id)

    return StandardResponse(
        success=True,
        message="获取我的任务成功",
        data={"tasks": [TaskResponse.from_orm(t).dict() for t in tasks]},
    )


@router.get("/{task_id}", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def get_task(
    task_id: int,
    current_user: CurrentUser = Depends(check_user_permission()),
    task_dao: TaskDAO = Depends(get_task_dao),
):
    """获取任务详情"""
    task = task_dao.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return StandardResponse(
        success=True, message="获取任务详情成功", data={"task": TaskResponse.from_orm(task).dict()}
    )


@router.put("/{task_id}", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: CurrentUser = Depends(check_user_permission()),
    task_dao: TaskDAO = Depends(get_task_dao),
):
    """更新任务"""
    task = task_dao.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 检查权限：只有创建者可以更新
    if task.creator_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="无权限修改此任务")

    update_data = task_data.dict(exclude_unset=True)
    success = task_dao.update_task(task_id, **update_data)

    if not success:
        raise HTTPException(status_code=500, detail="更新任务失败")

    updated_task = task_dao.get_task_by_id(task_id)
    return StandardResponse(
        success=True, message="任务更新成功", data={"task": TaskResponse.from_orm(updated_task).dict()}
    )


@router.delete("/{task_id}", response_model=StandardResponse)
@exception_wrapper(catch_http_exc=True)
async def delete_task(
    task_id: int,
    current_user: CurrentUser = Depends(check_user_permission()),
    task_dao: TaskDAO = Depends(get_task_dao),
):
    """删除任务"""
    task = task_dao.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 检查权限：只有创建者或管理员可以删除
    if task.creator_id != current_user.user_id and current_user.role not in [
        "admin",
        "super_admin",
    ]:
        raise HTTPException(status_code=403, detail="无权限删除此任务")

    success = task_dao.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除任务失败")

    return StandardResponse(success=True, message="任务删除成功", data={})
