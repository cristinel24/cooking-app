import os
from dotenv import load_dotenv

load_dotenv()

WAIT_ON_ERROR = 5
MAX_TIMEOUT_SECONDS = 3
BANNED_MASK = 0b1000

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "5000"))
HASHER_API_URL = os.getenv("HASHER_API_URL", "http://localhost:8202")
TOKEN_GENERATOR_API_URL = os.getenv("TOKEN_GENERATOR_API_URL", "http://localhost:8256")
USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "http://localhost:8234")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")


class Errors:
    INVALID_CREDS = 25601
    DB_ERROR = 25602
    HASH_ERROR = 25603
    DB_TIMEOUT = 25604
    TOKEN_ERROR = 25605
    UNKNOWN = 25606
    USER_RETRIEVER_ERROR = 25607


USER_PROJECTION = {
    "_id": 0,
    "id": 1,
    "roles": 1,
    "login": 1
}

