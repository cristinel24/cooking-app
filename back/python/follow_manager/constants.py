import os

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 7999)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "http://0.0.0.0:8000")
USER_CARDS_ROUTE = os.getenv("USER_CARDS_ROUTE", "/user-cards")

DUPLICATE_FOLLOW_ERROR = {
    "code": 21000
}

NONEXISTENT_FOLLOW_ERROR = {
    "code": 21001
}
