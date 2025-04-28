from uuid import UUID

from fastapi import HTTPException, status

from app.config.logs.logger import logger
from app.repository.activity_category import ActivityCategoryRepository
from app.schemas.activity_category import ActivityCategoryFullSchema
from app.services.base import BaseService


class ActivityCategoryService(BaseService):
    def __init__(self, activity_category_repository) -> None:
        self.activity_category_repository: ActivityCategoryRepository = (
            activity_category_repository
        )

    async def get_all_categories(self) -> list[ActivityCategoryFullSchema]:
        logger.info("Retrieving all activity categories")
        categories = await self.activity_category_repository.get_all_categories()
        return [
            ActivityCategoryFullSchema(**category.__dict__) for category in categories
        ]

    async def get_category_by_id(self, category_id: UUID) -> ActivityCategoryFullSchema:
        logger.info(f"Retrieving activity category with id: {category_id}")
        category = await self.activity_category_repository.get_category_by_id(
            category_id
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Activity category with id {category_id} not found",
            )
        return ActivityCategoryFullSchema(**category.__dict__)
