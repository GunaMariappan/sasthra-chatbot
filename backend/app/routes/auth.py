from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError, PyMongoError

from app.core.config import settings
from app.core.rate_limit import auth_rate_limit
from app.core.security import (
    DUMMY_HASH,
    create_access_token,
    hash_password,
    verify_password,
)
from app.db.mongodb import users_collection
from app.schemas.user import LoginRequest, SignupRequest, TokenResponse, UserResponse

router = APIRouter(tags=["Auth"])


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth_rate_limit)],
)
def signup(payload: SignupRequest):
    email = payload.email.lower()

    user_doc = {
        "name": payload.name,
        "email": email,
        "password_hash": hash_password(payload.password),
        "created_at": datetime.now(timezone.utc),
    }

    try:
        if users_collection.find_one({"email": email}):
            raise HTTPException(status_code=409, detail="Email already registered")
        result = users_collection.insert_one(user_doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Email already registered")
    except PyMongoError:
        raise HTTPException(status_code=503, detail="Database is unavailable")

    return {"id": str(result.inserted_id), "name": payload.name, "email": email}


@router.post(
    "/login",
    response_model=TokenResponse,
    dependencies=[Depends(auth_rate_limit)],
)
def login(payload: LoginRequest):
    if not settings.JWT_SECRET:
        raise HTTPException(status_code=500, detail="Server configuration error")

    email = payload.email.lower()

    try:
        user = users_collection.find_one({"email": email})
    except PyMongoError:
        raise HTTPException(status_code=503, detail="Database is unavailable")

    stored_hash = user["password_hash"] if user else DUMMY_HASH
    password_ok = verify_password(payload.password, stored_hash)

    if not user or not password_ok:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(str(user["_id"]))
    return {"access_token": token, "token_type": "bearer"}