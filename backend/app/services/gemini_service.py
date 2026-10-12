import logging
import time

import httpx

from app.core.config import settings

logger = logging.getLogger("uvicorn.error")

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

MAX_ATTEMPTS = 3  # 1 first try + 2 retries
RETRY_WAIT_SECONDS = 2
RETRYABLE_STATUS = {500, 503}

# error kind -> (HTTP status for our API, safe message for the user)
ERROR_RESPONSES = {
    "not_configured": (500, "Server configuration error"),
    "timeout": (504, "The AI service took too long to respond. Please try again."),
    "rate_limited": (429, "The AI service is busy. Please try again in a minute."),
    "overloaded": (503, "The AI service is busy right now. Please try again in a moment."),
    "blocked": (400, "This message could not be processed."),
    "network": (502, "The AI service is currently unavailable."),
    "api_error": (502, "The AI service is currently unavailable."),
    "bad_response": (502, "The AI service is currently unavailable."),
    "empty": (502, "The AI service returned an empty answer. Please try again."),
}


class GeminiError(Exception):
    """Our own error type. It never contains the API key."""

    def __init__(self, kind: str):
        super().__init__(kind)
        self.kind = kind


def generate_text(user_text: str, system_instruction: str | None = None) -> str:
    api_key = settings.GEMINI_API_KEY
    if not api_key or api_key.startswith("PASTE"):
        raise GeminiError("not_configured")

    url = f"{GEMINI_BASE_URL}/{settings.GEMINI_MODEL}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }
    body = {
        "contents": [{"role": "user", "parts": [{"text": user_text}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1024},
    }
    if settings.GEMINI_THINKING_LEVEL:
        body["generationConfig"]["thinkingConfig"] = {
            "thinkingLevel": settings.GEMINI_THINKING_LEVEL
        }
    if system_instruction:
        body["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    response = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = httpx.post(
                url,
                headers=headers,
                json=body,
                timeout=settings.GEMINI_TIMEOUT_SECONDS,
            )
        except httpx.TimeoutException:
            logger.warning("Gemini request timed out")
            raise GeminiError("timeout")
        except httpx.HTTPError:
            logger.warning("Gemini network error")
            raise GeminiError("network")

        if response.status_code in RETRYABLE_STATUS and attempt < MAX_ATTEMPTS:
            logger.warning(
                "Gemini returned %s, retrying (attempt %s of %s)",
                response.status_code,
                attempt,
                MAX_ATTEMPTS,
            )
            time.sleep(RETRY_WAIT_SECONDS)
            continue
        break

    if response.status_code == 429:
        logger.warning("Gemini quota or rate limit reached (429)")
        raise GeminiError("rate_limited")

    if response.status_code == 503:
        logger.warning("Gemini still overloaded (503) after retries")
        raise GeminiError("overloaded")

    if response.status_code != 200:
        logger.warning(
            "Gemini API returned status %s: %s",
            response.status_code,
            response.text[:300],
        )
        raise GeminiError("api_error")

    try:
        data = response.json()
    except ValueError:
        raise GeminiError("bad_response")

    if data.get("promptFeedback", {}).get("blockReason"):
        raise GeminiError("blocked")

    candidates = data.get("candidates") or []
    if not candidates:
        raise GeminiError("empty")

    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts if isinstance(p, dict)).strip()

    if not text:
        logger.warning(
            "Gemini empty text, finishReason=%s", candidates[0].get("finishReason")
        )
        raise GeminiError("empty")

    return text