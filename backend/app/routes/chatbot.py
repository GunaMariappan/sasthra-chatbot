from fastapi import APIRouter, Depends, HTTPException
from pymongo.errors import PyMongoError

from app.core.rate_limit import chat_rate_limit
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import chatbot_service
from app.services.gemini_service import ERROR_RESPONSES, GeminiError

router = APIRouter(tags=["Chatbot"])


@router.post("/chatbot", response_model=ChatResponse)
def chatbot(payload: ChatRequest, current_user: dict = Depends(chat_rate_limit)):
    try:
        answer = chatbot_service.get_answer(payload.message)
    except PyMongoError:
        raise HTTPException(status_code=503, detail="Database is unavailable")
    except GeminiError as exc:
        status_code, message = ERROR_RESPONSES.get(
            exc.kind, (502, "The AI service is currently unavailable.")
        )
        raise HTTPException(status_code=status_code, detail=message)

    return {"answer": answer}