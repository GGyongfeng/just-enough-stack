from typing import Optional

from pydantic import BaseModel


class UserType(BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    nickname: str
    register_token: str
    full_name: Optional[str] = None
    extra: Optional[str] = None

    class Config:
        from_attributes = True


class AgentType(BaseModel):
    id: Optional[int] = None
    agent_name: str
    agent_version: Optional[str] = None
    extra: Optional[str] = None

    class Config:
        from_attributes = True


class QueryCategoryType(BaseModel):
    id: Optional[int] = None
    name: str
    parent_id: Optional[int] = None
    level: int
    sort_order: Optional[int] = 0

    class Config:
        from_attributes = True


class QueryType(BaseModel):
    id: Optional[int] = None
    query_name: str
    category_id: Optional[int] = None
    lazy_query: str
    query_detail: Optional[str] = None
    extra: Optional[str] = None
    query_comment: Optional[str] = None
    creator_id: Optional[int] = None

    class Config:
        from_attributes = True


class EvaluationType(BaseModel):
    id: Optional[int] = None
    query_id: int
    agent_id: int
    trajectory: Optional[str] = None
    eval_report: Optional[str] = None
    eval_comment: Optional[str] = None
    total_score: Optional[float] = None
    comparable_items: Optional[str] = None
    extra: Optional[str] = None
    creator_id: Optional[int] = None

    class Config:
        from_attributes = True


class DeliverablesType(BaseModel):
    id: Optional[int] = None
    evaluation_id: int
    filename: str
    content: str  # base64 string
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    deliverables_comment: Optional[str] = None
    extra: Optional[str] = None

    class Config:
        from_attributes = True


class EvaluationStatDetailType(BaseModel):
    """评估统计详细信息响应模型"""

    # Evaluation 基础信息
    id: int
    evaluation_id: int
    query_id: int
    agent_id: int
    total_score: Optional[float] = None
    comparable_items: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # Query 相关信息
    query_name: str
    category_id: Optional[int] = None
    lazy_query: Optional[str] = None
    query_detail: Optional[str] = None
    query_extra: Optional[str] = None
    query_creator_id: Optional[int] = None
    query_creator_name: Optional[str] = None
    query_created_at: Optional[str] = None
    query_updated_at: Optional[str] = None

    # Agent 相关信息
    agent_name: str
    agent_version: Optional[str] = None
    agent_extra: Optional[str] = None

    class Config:
        from_attributes = True


class EvaluationStatListResponse(BaseModel):
    """评估统计列表响应模型"""

    evaluations: list[EvaluationStatDetailType]
    page: int
    size: int
    total: int
    query_filter: list[int]
    agent_filter: list[int]

    class Config:
        from_attributes = True
