from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

class UserRoles(int):
    VERIFIED = 0b1
    ADMIN = 0b10
    PREMIUM = 0b100
    BANNED = 0b1000
    ACTIVE = 0b0

HOST = os.getenv("HOST","localhost")
PORT = os.getenv("PORT","8000")
DB_NAME = os.getenv("DB_NAME")
MONGO_URI = os.getenv("MONGO_URI")
MAX_TIMEOUT_TIME_SECONDS = 3

class ErrorCodes(Enum):
    SERVER_ERROR = 21400
    NONEXISTENT_USER = 21401
    NONEXISTENT_ROLES = 21402
    FAILED_ROLES = 21403
