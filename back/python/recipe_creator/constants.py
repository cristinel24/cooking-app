import os
from enum import Enum, unique

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 7996))
HOST = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME", "cooking_app")

MAX_TIMEOUT_TIME_SECONDS = 3

ID_GENERATOR_API_URL = os.getenv("ID_GENERATOR_API_URL", "http://0.0.0.0:8002")
ID_GENERATOR_ROUTE = ID_GENERATOR_API_URL + "/"

AI_API_URL = os.getenv("AI_API_URL", "http://0.0.0.0:8003")
AI_RECIPE_TOKENIZER_ROUTE = AI_API_URL + ""

ALLERGEN_MANAGER_API_URL = os.getenv("ALLERGEN_MANAGER_API_URL", "http://0.0.0.0:8000")
INC_ALLERGENS_ROUTE = ALLERGEN_MANAGER_API_URL + "/allergens/inc"
DEC_ALLERGENS_ROUTE = ALLERGEN_MANAGER_API_URL + "/allergens/dec"

TAG_MANAGER_API_URL = os.getenv("TAG_MANAGER_API_URL", "http://0.0.0.0:8001")
INC_TAGS_ROUTE = TAG_MANAGER_API_URL + "/tags/inc"
DEC_TAGS_ROUTE = TAG_MANAGER_API_URL + "/tags/dec"


@unique
class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 26100
    DB_CONNECTION_TIMEOUT = 26101
    DB_CONNECTION_NONTIMEOUT = 26102
    NOT_RESPONSIVE_API = 26103
    INVALID_RECIPE_DATA = 26104
    NOT_AUTHENTICATED = 26105
