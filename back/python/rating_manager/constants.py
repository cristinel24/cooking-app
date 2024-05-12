from os import getenv
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = getenv("MONGO_URL",  "mongodb://localhost:27017?readPreference=secondary")

ID_GENERATOR_API_URL = getenv("ID_GENERATOR_API_URL")
if ID_GENERATOR_API_URL is None:
    raise ValueError("Environment variable 'ID_GENERATOR_API_URL' is not set")

USER_RETRIEVER_API_URL = getenv("USER_RETRIEVER_API_URL")
if USER_RETRIEVER_API_URL is None:
    raise ValueError("Environment variable 'USER_RETRIEVER_API_URL' is not set")


MONGO_DATABASE = "cooking_app"
MONGO_COLLECTION = "rating"

DELETED_FIELD = "[deleted]"


RATING_PROJECTION = {
    "_id": 0,
    "updatedAt": 1,
    "id": 1,
    "authorId": 1,
    "rating": 1,
    "description": 1,
    "children": 1,
    "parentId": 1,
    "parentType": 1,
}
