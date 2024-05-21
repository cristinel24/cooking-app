import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 7999))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "http://0.0.0.0:8000")

MAX_TIMEOUT_TIME_SECONDS = 3


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 21000
    DUPLICATE_FOLLOW = 21001
    NONEXISTENT_FOLLOW = 21002
    DB_CONNECTION_TIMEOUT = 21003
    DB_CONNECTION_NONTIMEOUT = 21004
    NOT_RESPONSIVE_API = 21005
    INVALID_USER = 21006
    NOT_AUTHENTICATED = 21007
    INVALID_FOLLOWS = 21008
