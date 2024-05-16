from enum import Enum

MAX_TIMEOUT_TIME_SECONDS = 3
NO_OF_RETURNED_ITEMS = 5


class ErrorCodes(Enum):
    SERVER_ERROR = 20800
    NONEXISTENT_ALLERGEN = 20801