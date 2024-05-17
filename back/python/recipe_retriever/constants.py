import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()
PORT = int(os.getenv("PORT", 8000))
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
USER_MICROSERVICE_URL = os.getenv("USER_MICROSERVICE_URL",
                                  "http://localhost:7998")
MAX_TIMEOUT_TIME_SECONDS = 3

RECIPE_DATA_PROJECTION = {
    "_id": 0,
    "authorId": 1,
    "title": 1,
    "description": 1,
    "prepTime": 1,
    "steps": 1,
    "ingredients": 1,
    "allergens": 1,
    "tags": 1,
    "thumbnail": 1,
    "viewCount": 1
}

RECIPE_DATA_CARD_PROJECTION = {
    "_id": 0,
    "authorId": 1,
    "title": 1,
    "description": 1,
    "prepTime": 1,
    "steps": 0,
    "ingredients": 0,
    "tags": 1,
    "allergens": 1,
    "thumbnail": 1,
    "viewCount": 1
}


class ErrorCodes(Enum):
    SERVER_ERROR = 20900
    NONEXISTENT_RECIPE = 20901
    FAILED_TO_GET_USER_CARD = 20902
    USER_NOT_FOUND = 21900

