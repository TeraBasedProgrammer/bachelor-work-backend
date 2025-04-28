from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request

from app.api.dependencies.services import get_billing_service
from app.api.dependencies.user import get_current_user
from app.models.user import User
from app.services.billing import BillingService

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post("/create-checkout-session")
async def create_checkout_session(
    credits_amount: Annotated[int, Body(..., embed=True)],
    current_user: User = Depends(get_current_user),
    billing_service: BillingService = Depends(get_billing_service),
) -> dict[str, str]:
    return await billing_service.create_checkout_session(credits_amount, current_user)


@router.post("/stripe-webhook")
async def stripe_webhook(
    request: Request,
    billing_service: BillingService = Depends(get_billing_service),
) -> None:
    return await billing_service.handle_stripe_webhook(request)
