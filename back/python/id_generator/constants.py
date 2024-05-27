import os
from enum import Enum, unique

from dotenv import load_dotenv

ID_PROJECTION = {"_id": 0, "value": 1}
MAX_TIMEOUT_TIME_SECONDS = 3  # 3 seconds timeout

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")


@unique
class ErrorCode(Enum):
    UNKNOWN = 20300
    DB_ERROR_ID_GENERATOR = 20301  # Failed to fetch or update the ID
    DB_ERROR_ACCESS = 20302  # Error accessing database
