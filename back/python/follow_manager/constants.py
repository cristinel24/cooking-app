
import os

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 7999)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "0.0.0.0")

FOLLOWERS_PROJECTION = {"_id": 0, "userId": 1}
FOLLOWING_PROJECTION = {"_id": 0, "followsId": 1}
