import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 8000)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
MAX_TIMEOUT_TIME_SECONDS = 3


class ErrorCodes(Enum):
    SERVER_ERROR = 20800
    SEARCH_HISTORY_NOT_FOUND = 20801
