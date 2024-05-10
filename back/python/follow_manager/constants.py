
import os

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 7999)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
