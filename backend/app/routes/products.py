from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo.errors import PyMongoError

from app.api.deps import get_current_user
from app.schemas.product import ProductResponse
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductResponse])
def get_all_products(current_user: dict = Depends(get_current_user)):
    try:
        return product_service.list_products()
    except PyMongoError:
        raise HTTPException(status_code=503, detail="Database is unavailable")


@router.get("/search", response_model=list[ProductResponse])
def search_products(
    q: str = Query(min_length=1, max_length=200),
    current_user: dict = Depends(get_current_user),
):
    try:
        return product_service.search_products(q)
    except PyMongoError:
        raise HTTPException(status_code=503, detail="Database is unavailable")


@router.get("/{slug}", response_model=ProductResponse)
def get_product(slug: str, current_user: dict = Depends(get_current_user)):
    try:
        product = product_service.get_product_by_slug(slug)
    except PyMongoError:
        raise HTTPException(status_code=503, detail="Database is unavailable")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product