from fastapi import APIRouter

from backend.user.router import router as user_router
from backend.auth.router import router as auth_router
from backend.task.router import router as task_router

router = APIRouter(prefix="/v1")

# router.include_router(user_router) # USER ROUTER ONLY FOR TEST
router.include_router(auth_router)
router.include_router(task_router)
