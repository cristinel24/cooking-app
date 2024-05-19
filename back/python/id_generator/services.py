from repository import MongoCollection

mongo_collection = None


def get_mongo_collection():
    global mongo_collection
    if mongo_collection is None:
        mongo_collection = MongoCollection()
    return mongo_collection


def get_next_id_services() -> int:
    collection = get_mongo_collection()
    return collection.get_next_id()
