"""
数据库连接工具
"""

from typing import Generator, Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker
from loguru import logger


def create_database_engine(
    database_url: str,
    echo: bool = False,
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_pre_ping: bool = True,
) -> Engine:
    """创建数据库引擎

    Args:
        database_url: 数据库连接 URL
        echo: 是否打印 SQL 语句
        pool_size: 连接池大小
        max_overflow: 连接池最大溢出数
        pool_pre_ping: 是否在使用前 ping 连接

    Returns:
        SQLAlchemy Engine 实例

    Examples:
        >>> # SQLite
        >>> engine = create_database_engine("sqlite:///./app.db")
        >>>
        >>> # PostgreSQL
        >>> engine = create_database_engine(
        ...     "postgresql://user:password@localhost/dbname",
        ...     pool_size=10
        ... )
        >>>
        >>> # MySQL
        >>> engine = create_database_engine(
        ...     "mysql+pymysql://user:password@localhost/dbname"
        ... )
    """
    logger.info(f"Creating database engine: {database_url.split('@')[-1] if '@' in database_url else database_url}")

    # SQLite 特殊处理
    if database_url.startswith("sqlite"):
        engine = create_engine(
            database_url,
            echo=echo,
            connect_args={"check_same_thread": False},  # SQLite 需要
        )
    else:
        engine = create_engine(
            database_url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=pool_pre_ping,
        )

    logger.info("Database engine created successfully")
    return engine


class DatabaseSessionManager:
    """数据库会话管理器

    使用单例模式管理 SQLAlchemy Session

    Examples:
        >>> from je_stack.utils import DatabaseSessionManager
        >>>
        >>> # 初始化
        >>> db_manager = DatabaseSessionManager("sqlite:///./app.db")
        >>>
        >>> # 获取 session
        >>> with db_manager.get_session() as session:
        ...     users = session.query(User).all()
        >>>
        >>> # 或者作为 FastAPI 依赖
        >>> @app.get("/users")
        >>> def get_users(session: Session = Depends(db_manager.get_session)):
        ...     return session.query(User).all()
    """

    def __init__(
        self,
        database_url: str,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        """初始化数据库会话管理器

        Args:
            database_url: 数据库连接 URL
            echo: 是否打印 SQL 语句
            pool_size: 连接池大小
            max_overflow: 连接池最大溢出数
        """
        self.engine = create_database_engine(
            database_url=database_url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

    def get_session(self) -> Generator[Session, None, None]:
        """获取数据库会话

        Yields:
            SQLAlchemy Session 实例

        Example:
            >>> with db_manager.get_session() as session:
            ...     user = session.query(User).first()
        """
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def create_all_tables(self, base) -> None:
        """创建所有表

        Args:
            base: SQLAlchemy DeclarativeBase 类

        Example:
            >>> from your_models import Base
            >>> db_manager.create_all_tables(Base)
        """
        logger.info("Creating all database tables...")
        base.metadata.create_all(bind=self.engine)
        logger.info("All tables created successfully")

    def drop_all_tables(self, base) -> None:
        """删除所有表（危险操作）

        Args:
            base: SQLAlchemy DeclarativeBase 类

        Warning:
            此操作会删除数据库中的所有表，请谨慎使用
        """
        logger.warning("Dropping all database tables...")
        base.metadata.drop_all(bind=self.engine)
        logger.warning("All tables dropped")


# 全局会话管理器（可选）
_db_manager: Optional[DatabaseSessionManager] = None


def get_db_session() -> Generator[Session, None, None]:
    """获取全局数据库会话（FastAPI 依赖注入使用）

    需要先调用 init_database() 初始化全局数据库管理器

    Yields:
        SQLAlchemy Session 实例

    Example:
        >>> from je_stack.utils import init_database, get_db_session
        >>> from fastapi import Depends
        >>>
        >>> # 在应用启动时初始化
        >>> init_database("sqlite:///./app.db")
        >>>
        >>> # 在路由中使用
        >>> @app.get("/users")
        >>> def get_users(session: Session = Depends(get_db_session)):
        ...     return session.query(User).all()
    """
    if _db_manager is None:
        raise RuntimeError(
            "Database not initialized. Call init_database() first."
        )
    yield from _db_manager.get_session()


def init_database(
    database_url: str,
    echo: bool = False,
    pool_size: int = 5,
    max_overflow: int = 10,
) -> DatabaseSessionManager:
    """初始化全局数据库管理器

    Args:
        database_url: 数据库连接 URL
        echo: 是否打印 SQL 语句
        pool_size: 连接池大小
        max_overflow: 连接池最大溢出数

    Returns:
        DatabaseSessionManager 实例

    Example:
        >>> from je_stack.utils import init_database
        >>>
        >>> db_manager = init_database("sqlite:///./app.db")
    """
    global _db_manager
    _db_manager = DatabaseSessionManager(
        database_url=database_url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
    )
    logger.info("Global database manager initialized")
    return _db_manager
