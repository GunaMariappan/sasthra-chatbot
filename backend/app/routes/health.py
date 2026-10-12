from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.db.mongodb import ping_database

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/health/db")
def database_health_check():
    if not ping_database():
        raise HTTPException(status_code=503, detail="Database is unavailable")
    return {"status": "ok", "database": "connected", "db_name": settings.DB_NAME}