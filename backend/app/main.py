import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import PyMongoError

from app.core.config import settings
from app.core.errors import register_error_handlers
from app.db.mongodb import create_indexes
from app.routes import auth, chatbot, health, products, users

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_indexes()
    except PyMongoError:
        logger.warning("Could not create MongoDB indexes. Is MongoDB running?")
    yield


is_production = settings.APP_ENV == "production"

app = FastAPI(
    title="Sasthra Product AI Chatbot",
    description="Domain-restricted chatbot API for Sasthra products",
    version="0.1.0",
    lifespan=lifespan,
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
    openapi_url=None if is_production else "/openapi.json",
)

# Order matters: the middleware added last is the outermost one.
register_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(chatbot.router)