from __future__ import annotations

from logging import getLogger
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import loguru

# 导入API路由
from src.api.v1 import router as router_v1

# 创建FastAPI应用
app = FastAPI(
    title="Just Enough Stack API",
    description="轻量级全栈开发框架 - 后端API服务",
    version="1.0.0",
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(router_v1, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return {"message": "Just Enough Stack API", "version": "1.0.0", "status": "running"}


@app.get("/api/v1/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "服务运行正常"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error_code": exc.status_code,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理器"""

    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "服务器内部错误", "error_code": 500},
    )


# Redirect uvicorn's logs
uvicorn_logger = getLogger("uvicorn.access")
uvicorn_logger.handlers.clear()


class LoguruHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        def replace_fields(record: loguru.Record):
            record["name"] = "uvicorn"
            record["function"] = "access"
            record["line"] = 0

        logger.patch(replace_fields).opt(exception=record.exc_info).log(
            level, record.getMessage()
        )


uvicorn_logger.addHandler(LoguruHandler())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
