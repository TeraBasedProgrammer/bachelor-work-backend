from datetime import datetime
from enum import Enum
from typing import Optional
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
    description: Optional[str] = None
    due_date: datetime


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    status: Optional[InvoiceStatus] = None
    cancellation_reason: Optional[str] = None


class InvoiceResponse(InvoiceBase):
    id: UUID
    status: InvoiceStatus
    cancellation_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
