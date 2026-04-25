from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Member(Base):
    __tablename__ = "member"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False)
    is_borrowing: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default="unban", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True)

    borrowings = relationship(
        "Borrowing", back_populates="member", cascade="all, delete-orphan")
