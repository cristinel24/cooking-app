import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 7996))
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")

ID_GENERATOR_API_URL = os.getenv("ID_GENERATOR_API_URL", "http://0.0.0.0:12345")
ID_GENERATOR_ROUTE = "/"

AI_API_URL = os.getenv("AI_API_URL", "http://0.0.0.0:8000")
AI_RECIPE_TOKENIZER_ROUTE = ""


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 26100
    NOT_RESPONSIVE_API = 26101
    INVALID_RECIPE_DATA = 26102
