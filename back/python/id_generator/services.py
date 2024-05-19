from repository import MongoCollection
from utils import base36encode

mongo_collection = None


def get_mongo_collection():
    global mongo_collection
    if mongo_collection is None:
        mongo_collection = MongoCollection()
    return mongo_collection


def get_next_id_services() -> str:
    collection = get_mongo_collection()
    return base36encode(collection.get_next_id())
