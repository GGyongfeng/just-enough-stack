"""
JE Stack - Just Enough Stack

A lightweight FastAPI framework with built-in authentication, permissions, and CRUD utilities.
"""

__version__ = "0.1.0"

# Import main modules
from . import auth
from . import crud
from . import schemas
from . import utils

# Import commonly used items for convenience
from .auth import (
    CurrentUser,
    create_token_for_user,
    hash_password,
    verify_password,
    check_user_permission,
)
from .crud import BaseDAO, FormValidationError
from .schemas import UserRole, StandardResponse
from .utils import setup_logger, get_db_session, create_database_engine

__all__ = [
    "__version__",
    # Modules
    "auth",
    "crud",
    "schemas",
    "utils",
    # Auth
    "CurrentUser",
    "create_token_for_user",
    "hash_password",
    "verify_password",
    "check_user_permission",
    # CRUD
    "BaseDAO",
    "FormValidationError",
    # Schemas
    "UserRole",
    "StandardResponse",
    # Utils
    "setup_logger",
    "get_db_session",
    "create_database_engine",
]
