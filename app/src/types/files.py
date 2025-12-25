from pydantic import BaseModel
from typing import Optional


# 用于 Base64 传输 (JSON API)
class FileDataModelBase64(BaseModel):
    filename: str
    content: str  # Base64 字符串
    encoding: str = "base64"
    file_type: str
    file_size: int
    extra: Optional[dict] = None


# 用于二进制传输 (multipart/form-data)
class FileDataModelRaw(BaseModel):
    filename: str
    content: bytes  # 原始字节
    file_type: str
    file_size: int
