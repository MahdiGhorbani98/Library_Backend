from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class BookCategory(Base):
    __tablename__ = "book_category"
    __table_args__ = (
        UniqueConstraint("book_id", "category_id", name="uq_book_category"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(
        ForeignKey("book.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"), nullable=False)

    book = relationship("Book", back_populates="book_category")
    category = relationship("Category", back_populates="book_category")
