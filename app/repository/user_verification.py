from typing import Optional
from uuid import UUID

from sqlalchemy import select

from app.models.user import User, UserVerification
from app.repository.base import BaseRepository
from app.schemas.user_verification import (
    UserVerificationCreateSchema,
    UserVerificationUpdate,
)


class UserVerificationRepository(BaseRepository):
    model = UserVerification

    async def get_verifications(
        self, status: Optional[str] = None
    ) -> list[UserVerification]:
        query = select(UserVerification)
        if status:
            query = query.where(UserVerification.status == status)
        return await self.get_many(query)

    async def create_verification(
        self, verification_data: UserVerificationCreateSchema
    ) -> UserVerification:
        user_verification: UserVerification = await self.create(verification_data)
        return user_verification

    async def get_verification_by_id(
        self, verification_id: UUID
    ) -> Optional[UserVerification]:
        query = select(UserVerification).where(UserVerification.id == verification_id)
        result: Optional[User] = await self.get_instance(query)

        return result

    async def get_by_user_id(self, user_id: UUID) -> list[UserVerification]:
        result = await self.get_many(
            select(UserVerification).where(UserVerification.user_id == user_id)
        )
        return result

    async def update_verification(
        self, verification_id: UUID, verification: UserVerificationUpdate
    ) -> Optional[UserVerification]:
        db_verification = await self.get_by_id(verification_id)
        if not db_verification:
            return None

        for field, value in verification.model_dump(exclude_unset=True).items():
            setattr(db_verification, field, value)

        await self.session.commit()
        await self.session.refresh(db_verification)
        return db_verification

    async def delete(self, verification_id: UUID) -> bool:
        db_verification = await self.get_by_id(verification_id)
        if not db_verification:
            return False

        await self.session.delete(db_verification)
        await self.session.commit()
        return True
