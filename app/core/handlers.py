from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from app.core.exceptions import (
    EntityNotFound,
    DuplicateResource,
    BadRequestError,
    InternalServerError,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(EntityNotFound)
    async def _handle_not_found(request: Request, exc: EntityNotFound):
        logger.info("Not found: %s", exc.detail)
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    @app.exception_handler(DuplicateResource)
    async def _handle_conflict(request: Request, exc: DuplicateResource):
        logger.info("Conflict: %s", exc.detail)
        return JSONResponse(status_code=409, content={"detail": exc.detail})

    @app.exception_handler(BadRequestError)
    async def _handle_bad_request(request: Request, exc: BadRequestError):
        logger.info("Bad request: %s", exc.detail)
        return JSONResponse(status_code=400, content={"detail": exc.detail})

    @app.exception_handler(InternalServerError)
    async def _handle_internal(request: Request, exc: InternalServerError):
        logger.exception("Internal error: %s", exc.detail)
        return JSONResponse(status_code=500, content={"detail": exc.detail})
