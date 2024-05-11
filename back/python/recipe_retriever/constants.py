import os

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 7998)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
USER_MICROSERVICE_URL = os.getenv("USER_MICROSERVICE_URL", "http://localhost:7998")