from datetime import datetime
from typing import Literal, Optional, Self
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.post import Post
from app.models.user import ServiceTypes
from app.schemas.activity_category import ActivityCategoryPostSchema


class PostBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: str
    service_price: float = Field(..., ge=0)
    service_type: Literal["S", "P"]
    category_ids: Optional[list[UUID]] = None
    user_id: Optional[UUID] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    service_price: Optional[float] = Field(None, ge=0)
    service_type: Optional[ServiceTypes] = None
    category_ids: Optional[list[UUID]] = None


class PostSchema(PostBase):
    id: UUID
    user_id: UUID
    number_of_views: int
    created_at: datetime
    updated_at: datetime
    categories: list[ActivityCategoryPostSchema]

    @classmethod
    def from_model(cls, obj: Post) -> Self:
        # Create a copy of the object's dict without activity_categories
        obj_dict = {k: v for k, v in obj.__dict__.items() if k != "categories"}

        return cls(
            **obj_dict,
            categories=(
                [
                    ActivityCategoryPostSchema(
                        id=category_post.category_id,
                        title=category_post.category.title,
                    )
                    for category_post in obj.categories
                ]
            ),
        )

    class Config:
        from_attributes = True
