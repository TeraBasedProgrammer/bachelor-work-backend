import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class InvoiceStatus(str, Enum):
    PENDING = "P"
    PAID = "A"
    CANCELLED = "C"


class LessonInvoice(Base):
    __tablename__ = "lesson_invoices"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    mentor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    mentee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[InvoiceStatus] = mapped_column(
        String(1),
        default=InvoiceStatus.PENDING.value,
        server_default=InvoiceStatus.PENDING.value,
    )
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cancellation_reason: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
