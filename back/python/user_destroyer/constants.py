import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 7998))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")

DELETED_USER_ID = "[deleted]"

MAX_TIMEOUT_TIME_SECONDS = 3


class UserRoles:
    VERIFIED = 0b1
    ADMIN = 0b10
    PREMIUM = 0b100
    BANNED = 0b1000
    ACTIVE = 0b0


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 217000
    NONEXISTENT_USER = 217001
    DB_CONNECTION_TIMEOUT = 21702
    DB_CONNECTION_NONTIMEOUT = 21703
    UNAUTHORIZED_REQUEST = 21704
    FORBIDDEN_REQUEST = 21705
    USER_ROLES_INVALID_VALUE = 21706
