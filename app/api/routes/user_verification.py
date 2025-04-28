from typing import Annotated, Any, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Form

from app.api.dependencies.auth import auth_wrapper
from app.api.dependencies.services import get_verification_service
from app.api.dependencies.user import get_current_user
from app.models.user import User
from app.schemas.user_verification import (
    UserVerificationCreateSchema,
    UserVerificationSchema,
)
from app.services.user_verification import UserVerificationService

router = APIRouter(prefix="/user-verification", tags=["user-verification"])


@router.post("/create")
async def create_verification(
    verification_data: Annotated[UserVerificationCreateSchema, Form()],
    current_user: User = Depends(get_current_user),
    verification_service: UserVerificationService = Depends(get_verification_service),
) -> None:
    return await verification_service.create_verification(
        verification_data, current_user
    )


@router.get("/{verification_id}")
async def get_verification(
    verification_id: UUID,
    _: dict[str, Any] = Depends(auth_wrapper),
    verification_service: UserVerificationService = Depends(get_verification_service),
) -> UserVerificationSchema:
    return await verification_service.get_verification(verification_id)


@router.get("/")
async def get_all_verifications(
    status: Optional[str] = None,
    verification_service: UserVerificationService = Depends(get_verification_service),
    _: dict[str, Any] = Depends(auth_wrapper),
) -> list[UserVerificationSchema]:
    return await verification_service.get_all_verifications(status)


@router.post("/{verification_id}/approve")
async def approve_verification(
    verification_id: UUID,
    verification_service: UserVerificationService = Depends(get_verification_service),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    _: dict[str, Any] = Depends(auth_wrapper),
) -> None:
    return await verification_service.approve_verification(
        verification_id, background_tasks
    )


@router.post("/{verification_id}/decline")
async def decline_verification(
    verification_id: UUID,
    reason: str = Body(..., embed=True),
    verification_service: UserVerificationService = Depends(get_verification_service),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    _: dict[str, Any] = Depends(auth_wrapper),
) -> None:
    return await verification_service.decline_verification(
        verification_id, background_tasks, reason
    )
