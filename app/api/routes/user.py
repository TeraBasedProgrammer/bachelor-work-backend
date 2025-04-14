from fastapi import APIRouter, BackgroundTasks, Body, Depends

from app.api.dependencies.services import get_user_service
from app.api.dependencies.user import get_current_user
from app.models.user import User
from app.schemas.user import (
    ForgotPasswordResetInput,
    LoginResponse,
    TokenData,
    UserFullSchema,
    UserLoginInput,
    UserSignUpInput,
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


@router.post("/auth/signup")
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
    return UserFullSchema(**current_user.__dict__)


# @router.patch("/{user_id}")
# async def update_user(user_id: str, user: User):
#     pass


# @router.delete("/{user_id}")
# async def delete_user(user_id: str):
#     pass
