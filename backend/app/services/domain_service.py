from dataclasses import dataclass, field

from app.core.text_utils import normalize_text, remove_stopwords
from app.services import product_service

BRAND_WORD = "sasthra"
MAX_CONTEXT_PRODUCTS = 10

GREETINGS = {
    "hi", "hii", "hello", "hey", "hai", "vanakkam",
    "good morning", "good afternoon", "good evening",
    "thanks", "thank you", "bye",
}

REJECT_MESSAGE = "Sorry, I can only answer questions related to Sasthra products."
GREETING_MESSAGE = (
    "Hello! I can answer questions about Sasthra products. What would you like to know?"
)


@dataclass
class DomainResult:
    status: str  # "greeting", "related", or "unrelated"
    reason: str
    products: list = field(default_factory=list)


def check_domain(question: str) -> DomainResult:
    normalized = normalize_text(question)

    # Layer 1: greeting
    if normalized in GREETINGS:
        return DomainResult("greeting", "Greeting, no AI call needed")

    # Layer 2a: a product name or alias is mentioned
    named = product_service.find_products_by_name(normalized)
    if named:
        return DomainResult("related", "Product name found in question", named)

    # Layer 2b: the brand word is mentioned
    if BRAND_WORD in normalized.split():
        products = product_service.list_products(limit=MAX_CONTEXT_PRODUCTS)
        return DomainResult("related", "Brand word 'sasthra' found", products)

    # Layer 3: does our approved data contain something relevant?
    search_text = remove_stopwords(normalized)
    if not search_text:
        return DomainResult("unrelated", "No meaningful words in the question")

    found = product_service.search_products(search_text)
    if found:
        return DomainResult(
            "related", "Matching product information found in database", found
        )

    return DomainResult("unrelated", "No matching product information in database")