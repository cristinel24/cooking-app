import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "http://localhost:7998")
MAX_TIMEOUT_TIME_SECONDS = 3

RECIPE_DATA_PROJECTION = {
    "_id": 1,
    "id": 1,
    "authorId": 1,
    "title": 1,
    "description": 1,
    "prepTime": 1,
    "steps": 1,
    "ingredients": 1,
    "allergens": 1,
    "tags": 1,
    "thumbnail": 1,
    "viewCount": 1,
    "ratingSum": 1,
    "ratingCount": 1,
    "updatedAt": 1,
}

RECIPE_DATA_CARD_PROJECTION = {
    "_id": 1,
    "id": 1,
    "authorId": 1,
    "title": 1,
    "description": 1,
    "prepTime": 1,
    "allergens": 1,
    "tags": 1,
    "thumbnail": 1,
    "viewCount": 1,
    "ratingSum": 1,
    "ratingCount": 1,
    "updatedAt": 1,
}


class ErrorCodes(Enum):
    SERVER_ERROR = 20900
    NONEXISTENT_RECIPE = 20901
    FAILED_TO_GET_USER_CARD = 20902
    USER_NOT_FOUND = 20903
    NON_RESPONSIVE_API = 20904
    BROKEN_USER_RETRIEVER_RESPONSE = 20905
