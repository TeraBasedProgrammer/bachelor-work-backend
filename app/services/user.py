import uuid
from typing import Any, Optional

from fastapi import BackgroundTasks, HTTPException, status
from google.auth.exceptions import MalformedError
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from app.config.logs.logger import logger
from app.config.settings.base import settings
from app.core.database import redis
from app.core.tasks import send_email_report_dashboard
from app.models.user import User
from app.repository.user import UserRepository
from app.schemas.user import (
    ForgotPasswordResetInput,
    LoginResponse,
    TokenData,
    UserLoginInput,
    UserSignUpInput,
)
from app.securities.auth_handler import auth_handler
from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, user_repository) -> None:
        self.user_repository: UserRepository = user_repository

    async def register_user(self, user_data: UserSignUpInput) -> LoginResponse:
        logger.info("Creating new User instance")

        # Hashing input password
        user_data.password = auth_handler.get_password_hash(user_data.password)

        try:
            result = await self.user_repository.create_user(user_data)
        except IntegrityError:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        logger.info("New user instance has been successfully created")
        return result

    async def authenticate_user(self, user_data: UserLoginInput) -> dict[str, Any]:
        logger.info(f'Login attempt with email "{user_data.email}"')

        user_existing_object = await self.user_repository.get_user_by_email(
            user_data.email
        )
        if not user_existing_object:
            logger.warning(
                f'User with email "{user_data.email}" is not registered in the system'
            )
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="User with this email is not registered in the system",
            )

        verify_password = auth_handler.verify_password(
            user_data.password, user_existing_object.password
        )
        if not verify_password:
            logger.warning("Invalid password was provided")
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Invalid password",
            )

        logger.info(f'User "{user_data.email}" successfully logged in the system')

        user_id = str(user_existing_object.id)
        auth_token = auth_handler.encode_token(user_id, user_data.email)
        return LoginResponse(token=auth_token)

    async def google_login(self, google_data: TokenData) -> LoginResponse:
        logger.info("Google login attempt")

        try:
            user_google_info = id_token.verify_oauth2_token(
                google_data.token, requests.Request(), settings.GOOGLE_AUTH_CLIENT_ID
            )
        except MalformedError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Google auth token",
            )

        if user_google_info["aud"] != settings.GOOGLE_AUTH_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Google auth token",
            )

        user_google_id = user_google_info["sub"]
        email = user_google_info.get("email")
        name = user_google_info.get("name")

        logger.critical(user_google_info)

        existing_user = await self.user_repository.get_user_by_email(email)

        if existing_user:
            if not existing_user.google_id:
                existing_user.google_id = user_google_id
                await self.user_repository.save(existing_user)
            elif existing_user.google_id != user_google_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Google account is already linked to another user",
                )

            auth_token = auth_handler.encode_token(existing_user.id, email)
            return LoginResponse(token=auth_token)

        logger.info("Creating new User instance")

        random_passsword = str(uuid.uuid4())
        new_user = User(
            email=email,
            name=name,
            google_id=user_google_id,
            password=auth_handler.get_password_hash(random_passsword),
        )

        await self.user_repository.save(new_user)

        auth_token = auth_handler.encode_token(new_user.id, email)
        return LoginResponse(token=auth_token)

    async def verify_forgot_password_token(self, token: str) -> None:
        if not await redis.get(token):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Invalid forgot password token",
            )

    async def forgot_password(
        self, user_email: str, background_tasks: BackgroundTasks
    ) -> None:
        user: Optional[User] = await self.user_repository.get_user_by_email(user_email)

        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="User with this email is not found",
            )

        user_full_name: str = user.name or "User"

        reset_code = str(uuid.uuid4())
        reset_link = f"{settings.WEB_URL}/en/forgot-password/reset/?token={reset_code}"

        await redis.set(reset_code, user_email, ex=3600)

        background_tasks.add_task(
            send_email_report_dashboard, user_email, user_full_name, reset_link
        )

    async def forgot_password_reset(self, reset_data: ForgotPasswordResetInput) -> None:
        await self.verify_forgot_password_token(reset_data.token)

        user_email: EmailStr = await redis.get(reset_data.token)
        user_to_update = await self.user_repository.get_user_by_email(user_email)

        user_to_update.password = auth_handler.get_password_hash(reset_data.password)

        await self.user_repository.save(user_to_update)
        logger.info("The password was successfully updated")

    # async def update_user_profile(
    #     self, current_user: User, data: UserUpdate
    # ) -> UserFullSchema:
    #     logger.info(f'Updating user profile of the user "{current_user}"')

    #     # Validate if data was provided
    #     self._validate_update_data(data)

    #     updated_user = await self.user_repository.update_user(current_user.id, data)

    #     logger.info(f'"{current_user}" profile was successfully updated')
    #     return await self.get_user_profile(updated_user)

    # async def reset_password(
    #     self, current_user: User, data: PasswordResetInput
    # ) -> PasswordChangeOutput:
    #     logger.info(f'Change password request from user "{current_user}"')

    #     # Validate the old password match the current one
    #     if not auth_handler.verify_password(data.old_password, current_user.password):
    #         logger.warning("Invalid old password was provided")
    #         raise HTTPException(
    #             status.HTTP_400_BAD_REQUEST,
    #             detail=error_wrapper("Invalid old password", "old_password"),
    #         )

    #     # Validate the new password does not match the old password
    #     if auth_handler.verify_password(data.new_password, current_user.password):
    #         logger.warning("Error: New password and old password are the same")
    #         raise HTTPException(
    #             status.HTTP_409_CONFLICT, detail="You can't use your old password"
    #         )

    #     current_user.password = auth_handler.get_password_hash(data.new_password)

    #     await self.user_repository.save(current_user)
    #     logger.info("The password was successfully updated")

    #     return PasswordChangeOutput(message="The password was successfully reset")
