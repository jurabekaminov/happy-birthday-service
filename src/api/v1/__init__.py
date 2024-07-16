from fastapi import APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.subscriptions import router as subscriptions_router
from src.api.v1.users import router as users_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(subscriptions_router)
