from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.services import get_invoice_service
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceUpdate
from app.services.invoice import InvoiceService

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice_data: InvoiceCreate,
    invoice_service: InvoiceService = Depends(get_invoice_service),
) -> InvoiceResponse:
    invoice = await invoice_service.create_invoice(invoice_data.model_dump())
    return invoice


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: UUID,
    invoice_service: InvoiceService = Depends(get_invoice_service),
) -> InvoiceResponse:
    invoice = await invoice_service.get_invoice_by_id(invoice_id)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    return invoice


@router.get("/mentor/{mentor_id}", response_model=list[InvoiceResponse])
async def get_mentor_invoices(
    mentor_id: UUID,
    invoice_service: InvoiceService = Depends(get_invoice_service),
) -> list[InvoiceResponse]:
    return await invoice_service.get_invoices_by_mentor_id(mentor_id)


@router.get("/mentee/{mentee_id}", response_model=list[InvoiceResponse])
async def get_mentee_invoices(
    mentee_id: UUID,
    invoice_service: InvoiceService = Depends(get_invoice_service),
) -> list[InvoiceResponse]:
    return await invoice_service.get_invoices_by_mentee_id(mentee_id)


@router.patch("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice_status(
    invoice_id: UUID,
    invoice_update: InvoiceUpdate,
    invoice_service: InvoiceService = Depends(get_invoice_service),
) -> InvoiceResponse:
    invoice = await invoice_service.update_invoice_status(
        invoice_id, invoice_update.status
    )
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    return invoice
