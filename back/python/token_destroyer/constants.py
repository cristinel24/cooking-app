from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")

MAX_TIMEOUT = 3


class ErrorCodes(Enum):
    TOKEN_NOT_FOUND = 22000
    FAILED_TO_DELETE_TOKEN = 22001
    NO_USERS_MATCHED = 22002
    FAILED_TO_UPDATE_USER = 22003
    DB_CONNECTION_TIMEOUT = 22004
    DB_CONNECTION_NONTIMEOUT = 22005
    UNKNOWN = 22006
    USER_NOT_FOUND = 22007

