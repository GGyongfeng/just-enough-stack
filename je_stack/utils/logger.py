"""
日志配置工具
"""

import sys
from loguru import logger
from typing import Optional


def setup_logger(
    level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "500 MB",
    retention: str = "10 days",
    format: Optional[str] = None,
) -> None:
    """配置 loguru 日志

    Args:
        level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        log_file: 日志文件路径（可选）
        rotation: 日志轮转大小或时间
        retention: 日志保留时间
        format: 自定义日志格式

    Example:
        >>> from je_stack.utils import setup_logger
        >>>
        >>> # 基本配置
        >>> setup_logger(level="DEBUG")
        >>>
        >>> # 输出到文件
        >>> setup_logger(
        ...     level="INFO",
        ...     log_file="logs/app.log",
        ...     rotation="100 MB",
        ...     retention="7 days"
        ... )
    """
    # 移除默认的 handler
    logger.remove()

    # 默认格式
    if format is None:
        format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

    # 添加控制台输出
    logger.add(
        sys.stderr,
        format=format,
        level=level,
        colorize=True,
    )

    # 添加文件输出（如果指定）
    if log_file:
        logger.add(
            log_file,
            format=format,
            level=level,
            rotation=rotation,
            retention=retention,
            encoding="utf-8",
        )

    logger.info(f"Logger initialized with level: {level}")
