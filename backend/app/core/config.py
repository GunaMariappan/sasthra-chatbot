import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_ENV = os.getenv("APP_ENV", "development").lower()

    MONGODB_URI = os.getenv("MONGODB_URI")
    DB_NAME = os.getenv("DB_NAME")

    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    GEMINI_TIMEOUT_SECONDS = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "30"))
    GEMINI_THINKING_LEVEL = os.getenv("GEMINI_THINKING_LEVEL", "")

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
        if origin.strip()
    ]

    RATE_LIMIT_AUTH_PER_MINUTE = int(os.getenv("RATE_LIMIT_AUTH_PER_MINUTE", "10"))
    RATE_LIMIT_CHAT_PER_MINUTE = int(os.getenv("RATE_LIMIT_CHAT_PER_MINUTE", "10"))


settings = Settings()

if not settings.MONGODB_URI or not settings.DB_NAME:
    raise RuntimeError("MONGODB_URI and DB_NAME must be set in backend/.env")

if not settings.JWT_SECRET or len(settings.JWT_SECRET) < 32:
    raise RuntimeError(
        "JWT_SECRET must be set in backend/.env and be at least 32 characters long"
    )

if settings.JWT_ALGORITHM not in {"HS256", "HS384", "HS512"}:
    raise RuntimeError("JWT_ALGORITHM must be HS256, HS384 or HS512")