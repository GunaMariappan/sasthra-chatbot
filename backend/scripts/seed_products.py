"""Loads SAMPLE Sasthra product data into MongoDB.

Run from the backend folder:
    python -m scripts.seed_products                  (load / update sample data)
    python -m scripts.seed_products --remove-sample  (delete sample data only)

ALL TEXT BELOW IS PLACEHOLDER SAMPLE DATA, NOT REAL SASTHRA INFORMATION.
Replace it with company-approved content before going live.
"""

import sys
from datetime import datetime, timezone

from app.db.mongodb import create_indexes, products_collection

SAMPLE_PRODUCTS = [
    {
        "slug": "sample-education-platform",
        "name": "Sasthra Education Platform [SAMPLE]",
        "category": "Education",
        "summary": "[SAMPLE DATA] Placeholder description of an education platform. "
        "Replace with approved Sasthra content.",
        "features": [
            "[SAMPLE] Course management",
            "[SAMPLE] Student progress tracking",
            "[SAMPLE] Online assessments",
        ],
        "services": [
            "[SAMPLE] Onboarding support",
            "[SAMPLE] Training sessions",
        ],
        "faqs": [
            {
                "question": "[SAMPLE] What is the Sasthra education platform?",
                "answer": "[SAMPLE] Placeholder answer. Replace with approved content.",
            },
            {
                "question": "[SAMPLE] How do students get started?",
                "answer": "[SAMPLE] Placeholder answer. Replace with approved content.",
            },
        ],
        "keywords": ["education", "courses", "students", "learning", "teachers"],
    },
    {
        "slug": "sample-platform-b",
        "name": "Sasthra Sample Platform B [SAMPLE]",
        "category": "General",
        "summary": "[SAMPLE DATA] Second placeholder product used to test search "
        "between multiple products.",
        "features": [
            "[SAMPLE] Reporting dashboard",
            "[SAMPLE] User management",
        ],
        "services": [
            "[SAMPLE] Technical support",
        ],
        "faqs": [
            {
                "question": "[SAMPLE] What reports are available?",
                "answer": "[SAMPLE] Placeholder answer. Replace with approved content.",
            },
        ],
        "keywords": ["reports", "dashboard", "management", "support"],
    },
]


def seed() -> None:
    create_indexes()
    now = datetime.now(timezone.utc)

    for product in SAMPLE_PRODUCTS:
        doc = {**product, "is_sample": True, "is_active": True, "updated_at": now}
        products_collection.update_one(
            {"slug": product["slug"]},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True,
        )

    print(f"Seeded {len(SAMPLE_PRODUCTS)} SAMPLE products.")


def remove_sample() -> None:
    result = products_collection.delete_many({"is_sample": True})
    print(f"Removed {result.deleted_count} sample products.")


if __name__ == "__main__":
    if "--remove-sample" in sys.argv:
        remove_sample()
    else:
        seed()