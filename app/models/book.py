from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    publication_year: Mapped[int | None] = mapped_column(
        Integer, nullable=True)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)
    is_available: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)

    borrowing = relationship(
        "Borrowing", back_populates="book", cascade="all, delete-orphan")
    book_author = relationship(
        "BookAuthor", back_populates="book", cascade="all, delete-orphan")
    book_category = relationship(
        "BookCategory", back_populates="book", cascade="all, delete-orphan")
