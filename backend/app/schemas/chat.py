from typing import Optional

from pydantic import BaseModel, Field, field_validator

MAX_MESSAGE_LENGTH = 500


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message cannot be empty")
        return value


class ChatResponse(BaseModel):
    answer: str


class DomainCheckResponse(BaseModel):
    status: str
    reason: str
    matched_products: list[str] = []
    reply: Optional[str] = None