import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "http://0.0.0.0:8000")
MAX_TIMEOUT_TIME_SECONDS = 3

HISTORY_MAX_SIZE = 100


class ErrorCodes(Enum):
    SERVER_ERROR = 21200
    SEARCH_HISTORY_EMPTY = 21201
    DB_CONNECTION_TIMEOUT = 21202
    DB_CONNECTION_FAILURE = 21203
    USER_NOT_FOUND = 21204
