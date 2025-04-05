import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ServicePriceTypes(str, Enum):
    PER_HOUR = "PH"
    PER_LESSON = "PL"


class ServiceTypes(str, Enum):
    SEEKING = "S"
    PROVIDING = "P"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20), unique=True, nullable=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(255), nullable=True)
    id_card_photo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    balance: Mapped[int] = mapped_column(default=0)
    cv_link: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    about_me_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    about_me_video_link: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    service_price: Mapped[float] = mapped_column(Float, nullable=True)
    service_price_type: Mapped[ServicePriceTypes] = mapped_column(
        SQLEnum(ServicePriceTypes), default=ServicePriceTypes.PER_LESSON
    )
    longitude: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    latitude: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    verifications: Mapped[list["UserVerification"]] = relationship(
        "UserVerification", back_populates="user"
    )
    activity_categories: Mapped[list["ActivityCategoryUser"]] = relationship(
        "ActivityCategoryUser", back_populates="user"
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class UserVerification(Base):
    __tablename__ = "user_verifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(2), nullable=False)
    admin_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="verifications")

    class Statuses(str, Enum):
        PENDING = "PD"
        APPROVED = "AP"
        DECLINED = "DC"

    def __repr__(self) -> str:
        return f"<UserVerification {self.id} for user {self.user_id}>"


class ActivityCategory(Base):
    __tablename__ = "activity_categories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    users: Mapped[list["ActivityCategoryUser"]] = relationship(
        "ActivityCategoryUser", back_populates="category"
    )

    def __repr__(self) -> str:
        return f"<ActivityCategory {self.title}>"


class ActivityCategoryUser(Base):
    __tablename__ = "activity_categories_users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activity_categories.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[ServiceTypes] = mapped_column(SQLEnum(ServiceTypes), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="activity_categories")
    category: Mapped["ActivityCategory"] = relationship(
        "ActivityCategory", back_populates="users"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id", "category_id", "type", name="unique_user_category_type"
        ),
    )

    def __repr__(self) -> str:
        return f"<ActivityCategoryUser {self.id} for user {self.user_id} and category {self.category_id}>"
