from fastapi import FastAPI

from app.core.database import engine
from app.models.base import Base
from app.models import member, book, author, category, borrowing, book_author, book_category

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Library backend is running"}
