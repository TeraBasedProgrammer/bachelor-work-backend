import stripe
from fastapi import HTTPException, Request

from app.config.logs.logger import logger
from app.config.settings.base import settings
from app.models.user import User
from app.repository.user import UserRepository
from app.services.base import BaseService


class BillingService(BaseService):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
        self.stripe_price_ids = {
            25: settings.STRIPE_25_CREDITS_PRICE_ID,
            200: settings.STRIPE_200_CREDITS_PRICE_ID,
            500: settings.STRIPE_500_CREDITS_PRICE_ID,
        }

    stripe.api_key = settings.STRIPE_SECRET_KEY

    async def create_checkout_session(
        self, credits_amount: int, current_user: User
    ) -> dict[str, str]:
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price": self.stripe_price_ids[credits_amount],
                        "quantity": 1,
                    }
                ],
                success_url=f"{settings.WEB_URL}/en/profile",
                cancel_url=f"{settings.WEB_URL}/en/profile",
                metadata={
                    "app_email": current_user.email,
                    "credits_amount": credits_amount,
                },
            )
            return {"session_id": checkout_session["id"]}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def handle_stripe_webhook(self, request: Request) -> None:
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            # Extract relevant data
            customer_email = session["metadata"]["app_email"]
            credits_amount = session["metadata"]["credits_amount"]

            user = await self.user_repository.get_user_by_email(customer_email)
            logger.debug(user.balance)

            user.balance += int(credits_amount)
            await self.user_repository.save(user)
            logger.debug(user.balance)
            logger.info(
                f"User {user.id} has been credited with {credits_amount} credits"
            )
