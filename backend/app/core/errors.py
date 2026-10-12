import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError

logger = logging.getLogger("uvicorn.error")


async def validation_error_handler(request: Request, exc: RequestValidationError):
    # Keep only type, loc and msg. Never echo the user's input back (it may be a password).
    errors = [
        {"type": e.get("type"), "loc": list(e.get("loc", [])), "msg": e.get("msg")}
        for e in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"detail": errors})


async def database_error_handler(request: Request, exc: PyMongoError):
    # Safety net for any database error that a route did not catch itself.
    logger.error(
        "Database error on %s %s: %s", request.method, request.url.path, type(exc).__name__
    )
    return JSONResponse(status_code=503, content={"detail": "Database is unavailable"})


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(PyMongoError, database_error_handler)

    @app.middleware("http")
    async def catch_unexpected_errors(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception:
            logger.exception("Unexpected error on %s %s", request.method, request.url.path)
            return JSONResponse(
                status_code=500,
                content={"detail": "Something went wrong on our side. Please try again later."},
            )