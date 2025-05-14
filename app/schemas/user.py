from datetime import datetime
from typing import Literal, Optional, Self
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, field_validator

from app.config.settings.base import settings
from app.models.user import ServicePriceTypes, User
from app.schemas.activity_category import ActivityCategoryUserSchema
from app.utilities.validation import (
    validate_name,
    validate_password,
    validate_phone_number,
)


class S3UrlMixin(BaseModel):
    @field_validator(
        "profile_picture",
        "id_card_photo",
        "about_me_video_link",
        "cv_link",
        mode="before",
        check_fields=False,
    )
    @classmethod
    def adjust_file_url(cls, value):
        if value is not None:
            return f"{settings.AWS_S3_ENDPOINT}/{value}"


class UserBaseSchema(S3UrlMixin):
    id: UUID
    email: str
    phone_number: Optional[str] = None
    name: str
    profile_picture: Optional[str] = None
    id_card_photo: Optional[str] = None
    verification_status: Literal["PD", "UV", "VR"]
    balance: int
    cv_link: Optional[str] = None
    about_me_text: Optional[str] = None
    about_me_video_link: Optional[str] = None
    service_price: Optional[float] = None
    service_price_type: ServicePriceTypes
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class UserFullSchema(UserBaseSchema):
    activity_categories: list[ActivityCategoryUserSchema]

    @classmethod
    def from_model(cls, obj: User) -> Self:
        # Create a copy of the object's dict without activity_categories
        obj_dict = {k: v for k, v in obj.__dict__.items() if k != "activity_categories"}

        return cls(
            **obj_dict,
            activity_categories=(
                [
                    ActivityCategoryUserSchema(
                        id=category_user.category_id,
                        type=category_user.type,
                        title=category_user.category.title,
                    )
                    for category_user in obj.activity_categories
                ]
            ),
        )

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    profile_picture: Optional[UploadFile | str] = None
    phone_number: Optional[str] = None
    activity_categories: Optional[list[str]] = None
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    id_card_photo: Optional[UploadFile | str] = None
    is_verified: Optional[bool] = None
    balance: Optional[int] = None
    cv_file: Optional[UploadFile | str] = None
    about_me_text: Optional[str] = None
    about_me_video_file: Optional[UploadFile | str] = None
    service_price: Optional[float] = None
    service_price_type: Optional[str] = None

    model_config = {"extra": "forbid"}


class TokenData(BaseModel):
    token: str


class LoginResponse(TokenData):
    user: UserFullSchema


class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone_number: str

    @field_validator("name")
    @classmethod
    def validate_user_name(cls, value):
        return validate_name(value)

    @field_validator("phone_number")
    @classmethod
    def validate_user_phone_number(cls, value):
        return validate_phone_number(value)


class UserSignUpInput(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return validate_password(value)


class UserLoginInput(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordResetInput(TokenData):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return validate_password(value)


class PasswordResetInput(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        return validate_password(value)
