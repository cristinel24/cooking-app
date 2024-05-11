import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 7998)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")

DELETED_USER_ID = "[deleted]"


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 217000
    NONEXISTENT_USER = 217001
    