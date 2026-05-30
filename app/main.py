from fastapi import FastAPI
# from app.api.member import router as member_router
from app.api.member import member_router
from app.core.database import engine
from app.models.base import Base
from app.core.handlers import register_exception_handlers
# from app.models import member, book, author, category, borrowing, book_author, book_category

app = FastAPI()

register_exception_handlers(app)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(member_router)


@app.get("/")
def root():
    return {"message": "Library backend is running"}
