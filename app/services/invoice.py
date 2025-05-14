from uuid import UUID

from app.models.invoice import InvoiceStatus, LessonInvoice
from app.repository.invoice import InvoiceRepository
from app.services.base import BaseService


class InvoiceService(BaseService):
    def __init__(self, invoice_repository: InvoiceRepository):
        self.invoice_repository = invoice_repository

    async def get_invoice_by_id(self, invoice_id: UUID) -> LessonInvoice | None:
        return await self.invoice_repository.get_invoice_by_id(invoice_id)

    async def get_invoices_by_mentor_id(self, mentor_id: UUID) -> list[LessonInvoice]:
        return await self.invoice_repository.get_invoices_by_mentor_id(mentor_id)

    async def get_invoices_by_mentee_id(self, mentee_id: UUID) -> list[LessonInvoice]:
        return await self.invoice_repository.get_invoices_by_mentee_id(mentee_id)

    async def create_invoice(self, invoice_data: dict) -> LessonInvoice:
        return await self.invoice_repository.create_invoice(invoice_data)

    async def update_invoice_status(
        self, invoice_id: UUID, status: InvoiceStatus
    ) -> LessonInvoice | None:
        return await self.invoice_repository.update_invoice_status(invoice_id, status)
