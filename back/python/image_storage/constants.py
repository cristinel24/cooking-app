import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 7997)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")

ID_GENERATOR_API_URL = os.getenv("ID_GENERATOR_API_URL", "http://0.0.0.0:8000")
ID_GENERATOR_ROUTE = os.getenv("ID_GENERATOR_ROUTE", "/")

IMAGE_DIRECTORY_PATH = "./images/"
IMAGE_EXTENSION = ".png"


class ErrorCodes(Enum):
    INVALID_IMAGE = 21300
    NOT_RESPONSIVE_API = 21301
    DUPLICATE_ID = 21302
