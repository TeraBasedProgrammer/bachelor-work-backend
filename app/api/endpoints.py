from fastapi import APIRouter

from app.api.routes.activity_category import router as activity_category_router
from app.api.routes.billing import router as billing_router
from app.api.routes.post import router as post_router
from app.api.routes.user import router as user_router
from app.api.routes.user_verification import router as user_verification_router

router = APIRouter()

router.include_router(user_router)
router.include_router(activity_category_router)
router.include_router(billing_router)
router.include_router(user_verification_router)
router.include_router(post_router)
