from typing import Optional
from uuid import UUID

from sqlalchemy import select

from app.models.invoice import InvoiceStatus, LessonInvoice
from app.repository.base import BaseRepository


class InvoiceRepository(BaseRepository):
    model = LessonInvoice

    async def get_invoice_by_id(self, invoice_id: UUID) -> Optional[LessonInvoice]:
        query = select(LessonInvoice).where(LessonInvoice.id == invoice_id)
        return await self.get_instance(query)

    async def get_invoices_by_mentor_id(self, mentor_id: UUID) -> list[LessonInvoice]:
        query = select(LessonInvoice).where(LessonInvoice.mentor_id == mentor_id)
        return await self.get_many(query)

    async def get_invoices_by_mentee_id(self, mentee_id: UUID) -> list[LessonInvoice]:
        query = select(LessonInvoice).where(LessonInvoice.mentee_id == mentee_id)
        return await self.get_many(query)

    async def create_invoice(self, invoice_data: dict) -> LessonInvoice:
        return await self.create(invoice_data)

    async def update_invoice_status(
        self, invoice_id: UUID, status: InvoiceStatus
    ) -> Optional[LessonInvoice]:
        invoice = await self.get_invoice_by_id(invoice_id)
        if invoice:
            invoice.status = status
            await self.save(invoice)
        return invoice
