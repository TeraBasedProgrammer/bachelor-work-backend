import uuid
from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, Field

from app.schemas.user import S3UrlMixin


class UserVerificationCreateSchema(BaseModel):
    user_id: uuid.UUID
    id_card_photo: Optional[UploadFile | str] = None
    about_me_text: Optional[str] = None
    about_me_video_link: Optional[UploadFile | str] = None
    cv_link: Optional[UploadFile | str] = None
    service_price: Optional[float] = None
    activity_categories: Optional[list[str]] = None
    service_price_type: Optional[Literal["PH", "PL"]] = None

    class Config:
        from_attributes = True


class UserVerificationSchema(UserVerificationCreateSchema, S3UrlMixin):
    id: uuid.UUID
    admin_id: Optional[uuid.UUID] = None
    status: Literal["PD", "AP", "DC"]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserVerificationUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=2)
    admin_id: Optional[UUID] = None
