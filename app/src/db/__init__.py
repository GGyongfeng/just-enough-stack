import os

from sqlalchemy import create_engine, text, inspect
from loguru import logger

from src.orm import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
engine = create_engine(DATABASE_URL, echo=False)

# Optimize large Blob field
if DATABASE_URL.startswith("sqlite"):
    inspector = inspect(engine)
    if not inspector.get_table_names():
        with engine.connect() as conn:
            conn.execute(text("PRAGMA page_size = 8192;"))
            conn.execute(text("VACUUM;"))
else:
    logger.warning("No BLOB optimization applied")

Base.metadata.create_all(engine)


__all__ = ["engine"]
