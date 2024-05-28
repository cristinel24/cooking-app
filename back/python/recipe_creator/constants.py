import os
from enum import Enum, unique

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 7996))
HOST = os.getenv("HOST_URL", "localhost")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")

MAX_TIMEOUT_TIME_SECONDS = 3

ID_GENERATOR_API_URL = os.getenv("ID_GENERATOR_API_URL", "http://localhost:8002")
ID_GENERATOR_ROUTE = ID_GENERATOR_API_URL + "/"

AI_API_URL = os.getenv("AI_API_URL", "http://localhost:8003")
AI_RECIPE_TOKENIZER_ROUTE = AI_API_URL + "/tokenize/recipe"

ALLERGEN_MANAGER_API_URL = os.getenv("ALLERGEN_MANAGER_API_URL", "http://localhost:8000")
INC_ALLERGENS_ROUTE = ALLERGEN_MANAGER_API_URL + "/allergens/inc"
DEC_ALLERGENS_ROUTE = ALLERGEN_MANAGER_API_URL + "/allergens/dec"

TAG_MANAGER_API_URL = os.getenv("TAG_MANAGER_API_URL", "http://localhost:8001")
INC_TAGS_ROUTE = TAG_MANAGER_API_URL + "/tags/inc"
DEC_TAGS_ROUTE = TAG_MANAGER_API_URL + "/tags/dec"

ALLOWED_TAGS = {"p", "ul", "li", "ol", "img", "s", "u", "strong", "em", "br"}
ALLOWED_ATTRIBUTES = {"img": {"src"}}
URL_SCHEMES = {"https", "http"}
UNSAFE_RECIPE_DATA_FIELDS = {"description", "steps"}


@unique
class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 26100
    DB_CONNECTION_TIMEOUT = 26101
    DB_CONNECTION_NONTIMEOUT = 26102
    NOT_RESPONSIVE_API = 26103
    UNAUTHORIZED_REQUEST = 26104
    INVALID_TITLE_SIZE = 26105
    INVALID_DESCRIPTION_SIZE = 26106
    INVALID_PREPTIME = 26107
    EMPTY_LIST_STEPS = 26108
    EMPTY_LIST_INGREDIENTS = 26109
    INVALID_THUMBNAIL_URL_SIZE = 26110
    MALFORMED_HTML = 26111
