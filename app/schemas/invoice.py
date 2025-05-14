from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class InvoiceStatus(str, Enum):
    PENDING = "P"
    PAID = "A"
    CANCELLED = "C"


class InvoiceBase(BaseModel):
    mentor_id: UUID
    mentee_id: UUID
    amount: int
    status: InvoiceStatus = InvoiceStatus.PENDING


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    status: InvoiceStatus


class InvoiceResponse(InvoiceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
