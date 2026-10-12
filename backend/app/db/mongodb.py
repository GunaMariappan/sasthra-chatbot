from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.core.config import settings

client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
db = client[settings.DB_NAME]

users_collection = db["users"]
products_collection = db["products"]


def ping_database() -> bool:
    try:
        client.admin.command("ping")
        return True
    except PyMongoError:
        return False


def create_indexes() -> None:
    users_collection.create_index("email", unique=True)

    products_collection.create_index("slug", unique=True)
    products_collection.create_index(
        [
            ("name", "text"),
            ("keywords", "text"),
            ("summary", "text"),
            ("features", "text"),
            ("services", "text"),
            ("faqs.question", "text"),
            ("faqs.answer", "text"),
        ],
        name="products_text_index",
        weights={
            "name": 10,
            "keywords": 8,
            "summary": 5,
            "features": 3,
            "services": 3,
            "faqs.question": 2,
            "faqs.answer": 1,
        },
    )