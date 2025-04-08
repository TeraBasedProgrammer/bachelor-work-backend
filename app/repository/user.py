from typing import Any, Optional

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.config.logs.logger import logger
from app.models.user import User
from app.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    async def create_user(self, user_data) -> dict[str, Any]:
        new_user: User = await self.create(user_data)

        logger.debug("Successfully inserted new user instance into the database")
        return {"id": new_user.id, "email": new_user.email}

    async def get_users(self) -> list[User]:
        result = await self.async_session.execute(
            select(User).options(joinedload(User.companies))
        )
        return result.unique().scalars().all()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = (
            select(User)
            .options(joinedload(User.tags), joinedload(User.companies))
            .where(User.id == user_id)
        )
        result: Optional[User] = await self.get_instance(query)
        if result:
            logger.debug(f'Retrieved user by id "{user_id}": "{result.id}"')
        return result

    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        query = select(User).where(User.email == email)
        result: Optional[User] = await self.get_instance(query)
        if result:
            logger.debug(f'Retrieved user by email "{email}": "{result.id}"')
        return result

    async def get_user_id(self, email: EmailStr) -> Optional[int]:
        query = select(User).where(User.email == email).with_only_columns(User.id)
        result: Optional[User] = await self.get_instance(query)
        if result:
            logger.debug(f'Retrieved user id by email "{email}": "{result}"')
        return result

    async def exists_by_email(self, email: EmailStr) -> bool:
        query = select(User).where(User.email == email)
        return await self.exists(query)

    async def update_user(self, user_id: int, user_data) -> User:
        updated_user = await self.update(user_id, user_data)

        logger.debug(f'Successfully updated user instance "{user_id}"')
        return updated_user

    async def delete_user(self, user_id: int) -> Optional[int]:
        result = await self.delete(user_id)

        logger.debug(f'Successfully deleted user "{result}" from the database')
        return result
