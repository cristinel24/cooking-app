import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8001))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
RECIPE_RETRIEVER_API_URL = os.getenv("RECIPE_RETRIEVER_API_URL", "http://localhost:8000")

MAX_TIMEOUT_TIME_SECONDS = 3


class ErrorCodes(Enum):
    SERVER_ERROR = 21500
    NONEXISTENT_USER = 21501
    NONEXISTENT_RECIPE = 21502
    RECIPE_ALREADY_SAVED = 21503
    RECIPE_NOT_SAVED = 21504
    UNAUTHORIZED_REQUEST = 21505
    FORBIDDEN_REQUEST = 21506
    NON_RESPONSIVE_API = 21507
