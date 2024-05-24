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

    def update_password(self, user_id: str, hash_alg_name: str, hashed_pass: str, salt: str) -> None:
        try:
            with timeout(TIMEOUT_LIMIT):
                self.connection.get_database(DB_NAME).user.update_one({"id": user_id},
                                                                      {"$set": {"login.hashAlgName": hash_alg_name,
                                                                                "login.hash": hashed_pass,
                                                                                "login.salt": salt}})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_UPDATE_PASSWORD.value)
