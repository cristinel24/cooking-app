import os
from enum import Enum, unique

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8187))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
AI_API_KEY = os.getenv("AI_API_KEY")
MESSAGE_HISTORY_MANAGER_API_URL = os.getenv("MESSAGE_HISTORY_MANAGER_API_URL")

GPT_MODEL = "gpt-3.5-turbo"

DB_TIMEOUT = 3


@unique
class ErrorCodes(Enum):
    AI_NOT_RESPONSIVE = 4100
    NO_SUCH_USER = 4101
    DB_CONNECTION_FAILURE = 4102
    DB_CONNECTION_TIMEOUT = 4103
    DB_CONNECTION_NON_TIMEOUT = 4104
    UNKNOWN = 4105
