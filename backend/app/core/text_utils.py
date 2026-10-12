import re

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "am",
    "do", "does", "did", "has", "have", "had",
    "what", "which", "who", "whom", "how", "when", "where", "why",
    "i", "me", "my", "we", "our", "you", "your", "it", "its",
    "this", "that", "there", "their", "they",
    "of", "to", "in", "on", "for", "at", "by", "from", "with", "about",
    "and", "or", "can", "could", "will", "would", "should",
    "tell", "give", "show", "please", "any", "some", "know", "want", "need", "like",
}


def normalize_text(text: str) -> str:
    """Lowercase, keep only letters/numbers/spaces, collapse extra spaces."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def remove_stopwords(text: str) -> str:
    """Remove common filler words and 1-letter words."""
    words = [w for w in text.split() if w not in STOPWORDS and len(w) > 1]
    return " ".join(words)