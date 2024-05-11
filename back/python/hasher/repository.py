import os
from pymongo import MongoClient
from constants import ErrorCodes


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
        try:
            self.connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
        except Exception:
            raise Exception(ErrorCodes.DB_CONNECTION_FAILURE.value)

    def get_primary_hash_algorithm_name(self) -> str:
        try:
            query_result = self.connection.cooking_app.hash_algorithm.find_one({"primary": {"$exists": True}}, {"name": 1})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_GET_PRIMARY_HASH_ALGO.value)
        return query_result["name"]

    def check_exists_hash_algorithm_name(self, name: str) -> bool:
        try:
            query_result = self.connection.cooking_app.hash_algorithm.find_one({"name": name}, {"_id": 1})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_CHECK_HASH_ALGO_EXISTANCE.value)
        return query_result is not None
