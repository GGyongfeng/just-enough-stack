# API v1 package
from fastapi import APIRouter

from .user import router as user_router
from .user_management import router as user_management_router
from .task import router as task_router

router = APIRouter()
router.include_router(user_router)
router.include_router(user_management_router)
router.include_router(task_router)
