from datetime import datetime
from typing import Literal, Optional, Self
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.post import Post
from app.models.user import ServiceTypes
from app.schemas.activity_category import ActivityCategoryPostSchema
from app.schemas.user import UserBaseSchema


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
    user: UserBaseSchema
    categories: list[ActivityCategoryPostSchema]

    @classmethod
    def from_model(cls, obj: Post) -> Self:
        # Create a copy of the object's dict without activity_categories
        obj_dict = {
            k: v for k, v in obj.__dict__.items() if k not in ["categories", "user"]
        }

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
            user=UserBaseSchema(**obj.user.__dict__),
        )

    class Config:
        from_attributes = True


class PostFilter(BaseModel):
    """Filter options for posts."""

    title: Optional[str] = None
    description: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    service_type: Optional[ServiceTypes] = None
    category_ids: Optional[list[UUID]] = None
    user_id: Optional[UUID] = None
    min_views: Optional[int] = None
    max_views: Optional[int] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None


class PaginatedResponse(BaseModel):
    items: list[PostSchema]
    total: int
    page: int
    per_page: int
    total_pages: int


class PostSort(BaseModel):
    """Sort options for posts."""

    field: Literal[
        "title", "service_price", "number_of_views", "created_at"
    ] = "created_at"
    order: Literal["asc", "desc"] = "desc"


class PostPagination(BaseModel):
    """Pagination options for posts."""

    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)


class PostQueryParams(PostFilter):
    """Combined query parameters for posts."""

    sort: Optional[PostSort] = None
    pagination: Optional[PostPagination] = None
