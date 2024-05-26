import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
USER_CARDS_ROUTE = "/user-cards"

MAX_TIMEOUT_TIME_SECONDS = 3

HISTORY_MAX_SIZE = 100


class ErrorCodes(Enum):
    SERVER_ERROR = 21100
    MESSAGE_HISTORY_NOT_FOUND = 21101
    DB_CONNECTION_TIMEOUT = 21102
    DB_CONNECTION_FAILURE = 21103
    USER_NOT_FOUND = 21104
