import os

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 8000)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME", "cooking_app")
FOLLOW_MANAGER_API_URL = os.getenv("FOLLOW_MANAGER_API_URL", "0.0.0.0")

USER_DATA_PROJECTION = {
    "_id": 0,
    "username": 1,
    "displayName": 1,
    "icon": 1,
    "roles": 1,
    "ratingSum": 1,
    "ratingCount": 1,
    "description": 1,
    "recipes": 1,
    "ratings": 1
}

USER_CARD_DATA_PROJECTION = {
    "_id": 0,
    "username": 1,
    "displayName": 1,
    "icon": 1,
    "roles": 1,
    "ratingSum": 1,
    "ratingCount": 1
}

USER_FULL_DATA_PROJECTION = {
    "_id": 0
}
