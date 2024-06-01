import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 7997))
HOST = os.getenv("HOST", "0.0.0.0")
GATEWAY_API_URL = os.getenv("GATEWAY_API_URL", "http://0.0.0.0:8000")
IMAGE_URL_HEAD = GATEWAY_API_URL + "/images/"

ID_GENERATOR_API_URL = os.getenv("ID_GENERATOR_API_URL", "http://0.0.0.0:12345")
ID_GENERATOR_ROUTE = "/"


IMAGE_DIRECTORY_PATH = "./images/"
ACCEPTED_IMAGE_FORMATS = [
    "PNG",
    "JPEG",
    "JPG",
]

MAX_IMAGE_SIZE = 16777216


class ErrorCodes(Enum):
    INVALID_IMAGE = 21300
    NOT_RESPONSIVE_API = 21301
    DUPLICATE_ID = 21302
    NONEXISTENT_IMAGE = 21303
    TOO_LARGE_FILE = 21304
    INVALID_IMAGE_FORMAT = 21305
