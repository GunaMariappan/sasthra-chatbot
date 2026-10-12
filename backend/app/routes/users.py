from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.schemas.user import UserResponse

router = APIRouter(tags=["Users"])


@router.get("/me", response_model=UserResponse)
def read_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "name": current_user["name"],
        "email": current_user["email"],
    }