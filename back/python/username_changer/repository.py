from pymongo import MongoClient, timeout
from constants import DB_NAME, MONGO_URI, TIMEOUT_LIMIT, ErrorCodes


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

    def update_username(self, user_id: str, new_username: str) -> None:
        try:
            with timeout(TIMEOUT_LIMIT):
                self.connection.get_database(DB_NAME).user.update_one({"id": user_id}, {"$set": {"username": new_username}})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_UPDATE_USERNAME.value)
