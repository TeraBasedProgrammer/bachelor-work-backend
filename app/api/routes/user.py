from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Form

from app.api.dependencies.services import get_user_service
from app.api.dependencies.user import get_current_user
from app.models.user import User
from app.schemas.user import (
    ForgotPasswordResetInput,
    LoginResponse,
    PasswordResetInput,
    TokenData,
    UserFullSchema,
    UserLoginInput,
    UserSignUpInput,
    UserUpdateSchema,
)
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/auth/login")
async def credentials_login(
    login_data: UserLoginInput,
    user_service: UserService = Depends(get_user_service),
) -> LoginResponse:
    return await user_service.authenticate_user(login_data)


@router.post("/auth/login/google")
async def google_login(
    token: TokenData,
    user_service: UserService = Depends(get_user_service),
) -> LoginResponse:
    return await user_service.google_login(token)


@router.post("/auth/sign-up")
async def register_user(
    sign_up_data: UserSignUpInput,
    user_service: UserService = Depends(get_user_service),
) -> LoginResponse:
    return await user_service.register_user(sign_up_data)


@router.post("/auth/forgot-password/request")
async def forgot_password(
    background_tasks: BackgroundTasks,
    email: str = Body(..., embed=True),
    user_service: UserService = Depends(get_user_service),
) -> None:
    return await user_service.forgot_password(email, background_tasks)


@router.post("/auth/forgot-password/verify-token")
async def verify_forgot_password_token(
    token: TokenData,
    user_service: UserService = Depends(get_user_service),
) -> None:
    return await user_service.verify_forgot_password_token(token.token)


@router.post("/auth/forgot-password/reset")
async def reset_password(
    reset_data: ForgotPasswordResetInput,
    user_service: UserService = Depends(get_user_service),
) -> None:
    return await user_service.forgot_password_reset(reset_data)


@router.get("/profile")
async def get_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserFullSchema:
    return UserFullSchema.from_model(current_user)


@router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
) -> UserFullSchema:
    return await user_service.get_user_by_id(user_id)


@router.patch("/{user_id}/update")
async def update_user(
    user_id: UUID,
    update_data: Annotated[UserUpdateSchema, Form()],
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> UserFullSchema:
    return await user_service.update_user(user_id, update_data, current_user)


@router.patch("/change-password")
async def change_password(
    reset_data: PasswordResetInput,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> None:
    return await user_service.reset_password(current_user, reset_data)
