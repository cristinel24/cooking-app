import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8090))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")


MAX_TIMEOUT_SECONDS = 3


TOKEN_TYPES = ["session", "usernameChange", "emailChange", "passwordChange", "emailConfirm"]
GET_EXPIRING_TOKEN = {"_id": 0, "roles": 1}


class Errors:
    INVALID_TYPE = 21603
    NOT_FOUND = 21604
    DB_ERROR = 21605
    DB_TIMEOUT = 21608
    UNKNOWN = 21609
