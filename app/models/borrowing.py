from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Borrowing(Base):
    __tablename__ = "borrowing"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(
        ForeignKey("member.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(
        ForeignKey("book.id"), nullable=False)
    borrowed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    returned_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True)
    status: Mapped[str] = mapped_column(
        String(30), default="onProgress", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True)

    member = relationship("Member", back_populates="borrowing")
    book = relationship("Book", back_populates="borrowing")
