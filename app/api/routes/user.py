from fastapi import APIRouter, Depends

from app.api.dependencies.services import get_user_service
from app.schemas.user import JwtToken, UserLoginInput, UserSignUpInput
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/auth/login")
async def credentials_login(
    login_data: UserLoginInput,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.authenticate_user(login_data)


@router.post("/auth/register")
async def register_user(
    sign_up_data: UserSignUpInput,
    user_service: UserService = Depends(get_user_service),
) -> JwtToken:
    return await user_service.register_user(sign_up_data)


# @router.patch("/{user_id}")
# async def update_user(user_id: str, user: User):
#     pass


# @router.delete("/{user_id}")
# async def delete_user(user_id: str):
#     pass
