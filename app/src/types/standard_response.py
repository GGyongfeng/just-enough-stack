from pydantic import BaseModel
from typing import Dict, Any


class StandardResponse(BaseModel):
    """标准响应模型"""

    success: bool
    message: str
    data: Dict[str, Any] | None = None
