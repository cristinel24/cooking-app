import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 7996))
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 26100
