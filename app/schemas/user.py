from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import ServicePriceTypes
from app.utilities.validation import (
    validate_name,
    validate_password,
    validate_phone_number,
)


class UserFullSchema(BaseModel):
    id: UUID
    email: str
    phone_number: Optional[str] = None
    name: str
    profile_picture: Optional[str] = None
    id_card_photo: Optional[str] = None
    is_verified: bool
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

    class Config:
        from_attributes = True


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
