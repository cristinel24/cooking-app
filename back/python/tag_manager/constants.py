import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")

MAX_TIMEOUT_TIME_SECONDS = 3
NO_OF_RETURNED_ITEMS = 5


class ErrorCodes(Enum):
    SERVER_ERROR = 20700
    NONEXISTENT_TAG = 20701
