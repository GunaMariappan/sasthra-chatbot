import logging
import time

from app.core.config import settings
from app.services import domain_service, prompt_service
from app.services.gemini_service import generate_text

logger = logging.getLogger("uvicorn.error")

SAFE_FALLBACK = "Sorry, I could not prepare an answer. Please try again."
MAX_ANSWER_CHARS = 3000

# If any of these appear in an answer, the model is leaking our prompt.
LEAK_MARKERS = ("<context>", "</context>", "<question>", "</question>", "SOURCE OF TRUTH")


def validate_answer(answer: str) -> str:
    answer = answer.strip()
    if not answer:
        return SAFE_FALLBACK

    secret_values = [s for s in (settings.GEMINI_API_KEY, settings.JWT_SECRET) if s]
    if any(secret in answer for secret in secret_values):
        logger.error("Gemini answer contained a secret value and was blocked")
        return SAFE_FALLBACK

    if any(marker in answer for marker in LEAK_MARKERS):
        logger.error("Gemini answer looked like a prompt leak and was blocked")
        return domain_service.REJECT_MESSAGE

    if len(answer) > MAX_ANSWER_CHARS:
        answer = answer[:MAX_ANSWER_CHARS].rstrip() + "..."
    return answer


def get_answer(question: str) -> str:
    result = domain_service.check_domain(question)
    logger.info(
        "Chat flow: domain=%s | reason=%s | products=%s",
        result.status,
        result.reason,
        [product["slug"] for product in result.products],
    )

    if result.status == "greeting":
        return domain_service.GREETING_MESSAGE

    if result.status == "unrelated":
        return domain_service.REJECT_MESSAGE

    if not result.products:
        return prompt_service.NO_INFO_MESSAGE

    context = prompt_service.build_context(result.products)
    prompt = prompt_service.build_user_prompt(question, context)

    started = time.perf_counter()
    answer = generate_text(prompt, system_instruction=prompt_service.SYSTEM_INSTRUCTION)
    logger.info("Chat flow: Gemini answered in %.1f s", time.perf_counter() - started)

    return validate_answer(answer)