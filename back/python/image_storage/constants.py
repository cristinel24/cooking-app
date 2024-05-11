import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 7997)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")

IMAGE_DIRECTORY_PATH = "./images/"
IMAGE_EXTENSION = ".png"


class ErrorCodes(Enum):
    INVALID_IMAGE = 21300
