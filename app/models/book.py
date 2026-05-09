from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
#! use uuid for primary key in book model
# import uuid
# from sqlalchemy.dialects.postgresql import UUID


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    #! use uuid for primary key in book model
    # id = Column(UUID(as_uuid=True), default=uuid.uuid4,
    #             primary_key=True, index=True)

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

    # Relationship to Borrowing records - enables book to track all borrowing instances
    # back_populates creates bidirectional relationship, cascade deletes child records when book is deleted
    borrowing = relationship(
        "Borrowing", back_populates="book", cascade="all, delete-orphan")
    
    # Relationship to BookAuthor - links book to its authors through an association table
    # cascade ensures associated records are deleted when book is deleted
    book_author = relationship(
        "BookAuthor", back_populates="book", cascade="all, delete-orphan")
    
    # Relationship to BookCategory - links book to its categories through an association table
    # cascade ensures associated records are deleted when book is deleted
    book_category = relationship(
        "BookCategory", back_populates="book", cascade="all, delete-orphan")
