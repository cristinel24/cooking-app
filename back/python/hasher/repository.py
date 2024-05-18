from constants import DB_NAME, MONGO_URI, TIMEOUT_LIMIT, ErrorCodes
from pymongo import MongoClient, timeout


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
            self.connection = MongoClient(MONGO_URI)
        except Exception:
            raise Exception(ErrorCodes.DB_CONNECTION_FAILURE.value)

    def get_primary_hash_algorithm_name(self) -> str:
        try:
            with timeout(TIMEOUT_LIMIT):
                query_result = self.connection.get_database(DB_NAME).hash_algorithm.find_one({"primary": {"$exists": True}}, {"name": 1})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_GET_PRIMARY_HASH_ALGO.value)
        return query_result["name"]

    def check_exists_hash_algorithm_name(self, name: str) -> bool:
        try:
            with timeout(TIMEOUT_LIMIT):
                query_result = self.connection.get_database(DB_NAME).hash_algorithm.find_one({"name": name}, {"_id": 1})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_CHECK_HASH_ALGO_EXISTANCE.value)
        return query_result is not None
