import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
ALLERGEN_MANAGER_API_URL = os.getenv("ALLERGEN_MANAGER_URL", "http://localhost:8001")
ADD_ALLERGENS = "/allergens/inc"
REMOVE_ALLERGENS = "/allergens/dec"
MONGO_TIMEOUT = 3

ICON_MAX_LENGTH = 2048
DISPLAY_NAME_MIN_LENGTH = 4
DISPLAY_NAME_MAX_LENGTH = 64
DESCRIPTION_MAX_LENGTH = 10000

ALLOWED_TAGS = {"p", "ul", "li", "ol", "img", "s", "u", "strong", "em", "br"}
ALLOWED_ATTRIBUTES = {"img": {"src"}}
URL_SCHEMES = {"https", "http"}


class ErrorCodes(Enum):
    USER_NOT_FOUND = 21800
    DATABASE_ERROR = 21801
    UNAUTHORIZED = 21802
    SERVER_ERROR = 21803
    ICON_SIZE_TOO_LARGE = 21804
    ICON_REQUIRED = 21805
    DISPLAY_NAME_TOO_LONG = 21806
    DISPLAY_NAME_TOO_SHORT = 21807
    DISPLAY_NAME_REQUIRED = 21808
    DESCRIPTION_REQUIRED = 21809
    DESCRIPTION_TOO_LONG = 21810
    MALFORMED_DESCRIPTION = 21811


ICON_VALIDATION = {
    "max_length": ICON_MAX_LENGTH,
    "too_long": ErrorCodes.ICON_SIZE_TOO_LARGE.value,
    "required": ErrorCodes.ICON_REQUIRED.value
}

DISPLAY_NAME_VALIDATION = {
    "min_length": DISPLAY_NAME_MIN_LENGTH,
    "max_length": DISPLAY_NAME_MAX_LENGTH,
    "too_short": ErrorCodes.DISPLAY_NAME_TOO_SHORT.value,
    "too_long": ErrorCodes.DISPLAY_NAME_TOO_LONG.value,
    "required": ErrorCodes.DISPLAY_NAME_REQUIRED.value
}

DESCRIPTION_VALIDATION = {
    "max_length": DESCRIPTION_MAX_LENGTH,
    "required": ErrorCodes.DESCRIPTION_REQUIRED.value,
    "too_long": ErrorCodes.DESCRIPTION_TOO_LONG.value
}
