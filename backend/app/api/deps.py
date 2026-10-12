import jwt
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pymongo.errors import PyMongoError

from app.core.security import decode_access_token
from app.db.mongodb import users_collection

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user_id = ObjectId(payload["sub"])
    except (InvalidId, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user = users_collection.find_one({"_id": user_id})
    except PyMongoError:
        raise HTTPException(status_code=503, detail="Database is unavailable")

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user