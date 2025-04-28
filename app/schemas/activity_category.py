from uuid import UUID

from pydantic import BaseModel


class ActivityCategoryBase(BaseModel):
    title: str


class ActivityCategoryCreate(ActivityCategoryBase):
    pass


class ActivityCategoryUpdate(ActivityCategoryBase):
    pass


class ActivityCategoryFullSchema(ActivityCategoryBase):
    id: UUID


class ActivityCategoryUserSchema(BaseModel):
    id: UUID
    title: str
    type: str
