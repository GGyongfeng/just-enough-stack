"""任务相关的 Pydantic 模型"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """创建任务的请求模型"""

    title: str = Field(..., min_length=1, max_length=200, description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")
    status: str = Field(default="pending", description="任务状态")
    priority: str = Field(default="medium", description="任务优先级")
    due_date: Optional[datetime] = Field(None, description="截止日期")


class TaskUpdate(BaseModel):
    """更新任务的请求模型"""

    title: Optional[str] = Field(None, min_length=1, max_length=200, description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")
    status: Optional[str] = Field(None, description="任务状态")
    priority: Optional[str] = Field(None, description="任务优先级")
    due_date: Optional[datetime] = Field(None, description="截止日期")


class TaskResponse(BaseModel):
    """任务响应模型"""

    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    creator_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
