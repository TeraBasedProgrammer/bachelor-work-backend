import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.user import User


class PaymentTypes(str, Enum):
    GOOGLE_PAY = "GP"
    CREDIT_CARD = "CC"


class TransactionStatuses(str, Enum):
    PENDING = "PE"
    SUCCESS = "SS"
    CANCELED = "CD"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    credits_amount: Mapped[int] = mapped_column(nullable=False)
    payment_type: Mapped[PaymentTypes] = mapped_column(String(2), nullable=False)
    status: Mapped[TransactionStatuses] = mapped_column(String(2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<Transaction {self.id}>"
