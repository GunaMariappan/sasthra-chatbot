import re
from typing import Optional

from app.core.text_utils import normalize_text
from app.db.mongodb import products_collection


def list_products(limit: int = 50) -> list[dict]:
    cursor = (
        products_collection.find({"is_active": True}, {"_id": 0})
        .sort("name", 1)
        .limit(limit)
    )
    return list(cursor)


def get_product_by_slug(slug: str) -> Optional[dict]:
    return products_collection.find_one({"slug": slug, "is_active": True}, {"_id": 0})


def search_products(query: str, limit: int = 3) -> list[dict]:
    # Cleaning removes MongoDB search operators such as "-word" and quotes.
    query = normalize_text(query)
    if not query:
        return []

    cursor = (
        products_collection.find(
            {"$text": {"$search": query}, "is_active": True},
            {"_id": 0, "score": {"$meta": "textScore"}},
        )
        .sort([("score", {"$meta": "textScore"})])
        .limit(limit)
    )
    return list(cursor)


def find_products_by_name(normalized_question: str) -> list[dict]:
    """Return products whose name (or alias) appears in the question."""
    padded = f" {normalized_question} "
    matches = []

    for product in list_products():
        names = [product["name"], *product.get("aliases", [])]
        for name in names:
            alias = normalize_text(re.sub(r"\[.*?\]", " ", name))
            if alias and f" {alias} " in padded:
                matches.append(product)
                break

    return matches