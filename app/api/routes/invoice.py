from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies.services import get_invoice_service
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceUpdate
from app.services.invoice import InvoiceService

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice_data: InvoiceCreate,
    invoice_service: InvoiceService = Depends(get_invoice_service),
) -> None:
    await invoice_service.create_invoice(invoice_data)


@router.get("/mentor/{mentor_id}", response_model=list[InvoiceResponse])
async def get_mentor_invoices(
    mentor_id: UUID,
    invoice_service: InvoiceService = Depends(get_invoice_service),
) -> list[InvoiceResponse]:
    return await invoice_service.get_invoices_by_mentor_id(mentor_id)


@router.patch("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: UUID,
    invoice_update: InvoiceUpdate,
    invoice_service: InvoiceService = Depends(get_invoice_service),
) -> InvoiceResponse:
    return await invoice_service.update_invoice(invoice_id, invoice_update)
