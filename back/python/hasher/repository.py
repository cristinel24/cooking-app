import os
from pymongo import MongoClient


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class DBWrapper:
    def __init__(self):
        self.connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))

    def get_primary_hash_algorithm_name(self) -> str:
        query_result = self.connection.cooking_app.hash_algorithm.find_one({"primary": {"$exists": True}}, {"name": 1})
        return query_result["name"]

    def check_exists_hash_algorithm_name(self, name: str) -> bool:
        query_result = self.connection.cooking_app.hash_algorithm.find_one({"name": name}, {"_id": 1})
        return query_result is not None
