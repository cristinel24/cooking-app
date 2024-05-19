import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("TOKEN_GENERATOR_URL", "localhost")
PORT = int(os.getenv("PORT", "8090"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")

TOKEN_TYPES = ["session", "usernameChange", "emailChange", "passwordChange", "emailConfirm"]

MAX_TIMEOUT_SECONDS = 3


class Errors:
    USER_NOT_FOUND = 20404
    INVALID_TYPE = 20400
    DATABASE_ERROR = 20405
    DB_TIMEOUT = 20413
