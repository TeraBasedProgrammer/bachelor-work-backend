import json
from typing import Optional
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException, status

from app.core.tasks import (
    send_email_approve_verification,
    send_email_decline_verification,
)
from app.models.user import (
    ActivityCategoryUser,
    MentorVerificationStatus,
    ServiceTypes,
    User,
    UserVerificationStatus,
)
from app.repository.user import UserRepository
from app.repository.user_verification import UserVerificationRepository
from app.schemas.user_verification import (
    UserVerificationCreateSchema,
    UserVerificationSchema,
)
from app.services.base import BaseService


class UserVerificationService(BaseService):
    def __init__(
        self,
        verification_repository: UserVerificationRepository,
        user_repository: UserRepository,
    ):
        self.verification_repository = verification_repository
        self.user_repository = user_repository

    async def create_verification(
        self, verification_data: UserVerificationCreateSchema, current_user: User
    ) -> None:
        """
        Create a new user verification.
        """

        if verification_data.activity_categories:
            verification_data.activity_categories = json.loads(
                verification_data.activity_categories[0]
            )

        upload_tasks = [
            ("id_card_photo", "id_card_photo.jpg"),
            ("about_me_video_link", "about_me_video_link.mp4"),
            ("cv_link", "cv_link.pdf"),
        ]

        # Upload files to S3
        await self._upload_files_to_s3(verification_data, upload_tasks)

        await self.verification_repository.create_verification(verification_data)

        current_user.verification_status = UserVerificationStatus.PENDING.value
        await self.user_repository.save(current_user)

    async def get_verification(
        self, verification_id: UUID
    ) -> Optional[UserVerificationSchema]:
        """
        Get a specific verification by its ID.
        """
        return await self.verification_repository.get_verification_by_id(
            verification_id
        )

    async def get_user_verifications(
        self, user_id: UUID
    ) -> list[UserVerificationSchema]:
        """
        Get all verification requests for a specific user.
        """
        return await self.verification_repository.get_by_user_id(user_id)

    async def get_all_verifications(
        self, status: Optional[str] = None
    ) -> list[UserVerificationSchema]:
        """
        Get all verification requests in the system.
        """
        return await self.verification_repository.get_verifications(status)

    async def approve_verification(
        self, verification_id: UUID, background_tasks: BackgroundTasks
    ) -> None:
        """
        Approve a verification request.
        """
        verification = await self.verification_repository.get_verification_by_id(
            verification_id
        )
        if not verification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Verification not found"
            )

        verification.status = UserVerificationStatus.APPROVED.value
        await self.verification_repository.save(verification)

        verification_user: User = await self.user_repository.get_user_by_id(
            verification.user_id
        )

        verification_user.verification_status = MentorVerificationStatus.VERIFIED.value
        verification_user.id_card_photo = verification.id_card_photo
        verification_user.about_me_text = verification.about_me_text
        verification_user.about_me_video_link = verification.about_me_video_link
        verification_user.cv_link = verification.cv_link
        verification_user.service_price = verification.service_price
        verification_user.service_price_type = verification.service_price_type

        await self.user_repository.clean_activity_categories(verification_user.id)

        new_activity_categories = [
            ActivityCategoryUser(
                user_id=verification_user.id,
                category_id=category_id,
                type=ServiceTypes.PROVIDING.value,
            )
            for category_id in verification.activity_categories
        ]

        await self.user_repository.save_many(new_activity_categories)

        await self.user_repository.save(verification_user)

        background_tasks.add_task(
            send_email_approve_verification,
            verification_user.email,
            verification_user.name,
        )

    async def decline_verification(
        self, verification_id: UUID, background_tasks: BackgroundTasks, reason: str
    ) -> None:
        """
        Decline a verification request.
        """
        verification = await self.verification_repository.get_verification_by_id(
            verification_id
        )
        if not verification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Verification not found"
            )

        verification_user: User = await self.user_repository.get_user_by_id(
            verification.user_id
        )
        verification_user.verification_status = (
            MentorVerificationStatus.UNVERIFIED.value
        )
        await self.user_repository.save(verification_user)

        verification.status = UserVerificationStatus.DECLINED.value
        await self.verification_repository.save(verification)

        background_tasks.add_task(
            send_email_decline_verification,
            verification.user.email,
            verification.user.name,
            reason,
        )
