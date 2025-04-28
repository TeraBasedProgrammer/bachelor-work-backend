from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import auth_wrapper
from app.api.dependencies.services import get_activity_category_service
from app.schemas.activity_category import ActivityCategoryFullSchema
from app.services.activity_category import ActivityCategoryService

router = APIRouter(prefix="/activity-categories", tags=["activity-categories"])


@router.get("/", response_model=list[ActivityCategoryFullSchema])
async def get_all_categories(
    activity_category_service: ActivityCategoryService = Depends(
        get_activity_category_service
    ),
    _: dict[str, Any] = Depends(auth_wrapper),
) -> list[ActivityCategoryFullSchema]:
    return await activity_category_service.get_all_categories()


@router.get("/{category_id}", response_model=ActivityCategoryFullSchema)
async def get_category_by_id(
    category_id: UUID,
    activity_category_service: ActivityCategoryService = Depends(
        get_activity_category_service
    ),
    _: dict[str, Any] = Depends(auth_wrapper),
) -> ActivityCategoryFullSchema:
    return await activity_category_service.get_category_by_id(category_id)
