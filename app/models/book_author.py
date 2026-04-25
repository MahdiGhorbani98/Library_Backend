from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class BookAuthor(Base):
    __tablename__ = "book_author"
    __table_args__ = (
        UniqueConstraint("book_id", "author_id", name="uq_book_author"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(
        ForeignKey("book.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("author.id"), nullable=False)

    book = relationship("Book", back_populates="book_author")
    author = relationship("Author", back_populates="book_author")
