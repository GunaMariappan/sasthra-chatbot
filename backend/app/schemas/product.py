from typing import Optional

from pydantic import BaseModel


class FaqItem(BaseModel):
    question: str
    answer: str


class ProductResponse(BaseModel):
    slug: str
    name: str
    category: str
    summary: str
    features: list[str] = []
    services: list[str] = []
    faqs: list[FaqItem] = []
    keywords: list[str] = []
    is_sample: bool = False
    score: Optional[float] = None