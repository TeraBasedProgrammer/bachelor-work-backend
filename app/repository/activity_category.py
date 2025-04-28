from typing import Optional
from uuid import UUID

from sqlalchemy import select

from app.config.logs.logger import logger
from app.models.user import ActivityCategory
from app.repository.base import BaseRepository


class ActivityCategoryRepository(BaseRepository):
    model = ActivityCategory

    async def get_all_categories(self) -> list[ActivityCategory]:
        categories = await self.get_many(select(ActivityCategory))
        logger.debug(f"Retrieved {len(categories)} activity categories")
        return categories

    async def get_category_by_id(self, category_id: UUID) -> Optional[ActivityCategory]:
        query = select(ActivityCategory).where(ActivityCategory.id == category_id)
        result: Optional[ActivityCategory] = await self.get_instance(query)
        if result:
            logger.debug(f'Retrieved activity category by id "{category_id}"')
        return result
