from uuid import UUID

from fastapi import HTTPException

from app.models.invoice import InvoiceStatus, LessonInvoice
from app.repository.invoice import InvoiceRepository
from app.repository.user import UserRepository
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate
from app.services.base import BaseService


class InvoiceService(BaseService):
    def __init__(
        self,
        invoice_repository: InvoiceRepository,
        user_repository: UserRepository,
    ):
        self.invoice_repository = invoice_repository
        self.user_repository = user_repository

    async def get_invoices_by_mentor_id(self, mentor_id: UUID) -> list[LessonInvoice]:
        return await self.invoice_repository.get_invoices_by_mentor_id(mentor_id)

    async def create_invoice(self, invoice_data: InvoiceCreate) -> LessonInvoice:
        mentor_user = await self.user_repository.get_user_by_id(invoice_data.mentor_id)
        if not mentor_user:
            raise HTTPException(status_code=404, detail="Mentor not found")

        mentee_user = await self.user_repository.get_user_by_id(invoice_data.mentee_id)
        if not mentee_user:
            raise HTTPException(status_code=404, detail="Mentee not found")

        if mentee_user.balance < invoice_data.amount:
            raise HTTPException(
                status_code=400, detail="Mentee does not have enough balance"
            )

        mentee_user.balance -= invoice_data.amount
        await self.user_repository.save(mentee_user)

        await self.invoice_repository.create_invoice(invoice_data)

    async def update_invoice(
        self, invoice_id: UUID, update_data: InvoiceUpdate
    ) -> LessonInvoice | None:
        invoice = await self.invoice_repository.get_invoice_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        if invoice.status == InvoiceStatus.PAID:
            raise HTTPException(status_code=400, detail="Invoice already paid")

        if (
            update_data.status == InvoiceStatus.CANCELLED
            and update_data.cancellation_reason
        ):
            invoice.cancellation_reason = update_data.cancellation_reason

        if update_data.status == InvoiceStatus.PAID:
            mentor_user = await self.user_repository.get_user_by_id(invoice.mentor_id)
            if not mentor_user:
                raise HTTPException(status_code=404, detail="Mentor not found")

            mentor_user.balance += invoice.amount
            await self.user_repository.save(mentor_user)

        invoice.status = update_data.status

        await self.invoice_repository.save(invoice)
        return invoice
