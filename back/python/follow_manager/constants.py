import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 7999)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "http://0.0.0.0:8000")
USER_CARDS_ROUTE = os.getenv("USER_CARDS_ROUTE", "/user-cards")

MAX_TIMEOUT_TIME_SECONDS = 3


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 21000
    DUPLICATE_FOLLOW = 21001
    NONEXISTENT_FOLLOW = 21002
    DB_CONNECTION_TIMEOUT = 21003
    DB_CONNECTION_NONTIMEOUT = 21004
    NOT_RESPONSIVE_API = 21005
