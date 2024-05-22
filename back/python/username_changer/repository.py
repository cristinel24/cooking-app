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

    def get_token_type(self, token: str) -> str:
        try:
            with timeout(TIMEOUT_LIMIT):
                query_result = self.connection.get_database(DB_NAME).expiring_token.find_one({"value": token}, {"tokenType": 1})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_GET_TOKEN_TYPE.value)
        if query_result is None or "tokenType" not in query_result:
            raise Exception(ErrorCodes.TOKEN_NOT_FOUND.value)
        return query_result["tokenType"]

    def get_user_id(self, token: str) -> str:
        try:
            with timeout(TIMEOUT_LIMIT):
                query_result = self.connection.get_database(DB_NAME).expiring_token.find_one({"value": token}, {"userId": 1})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_GET_USER_ID.value)
        if query_result is None or "userId" not in query_result:
            raise Exception(ErrorCodes.USER_NOT_FOUND.value)
        return query_result["userId"]

    def update_username(self, user_id: str, new_username: str) -> None:
        try:
            with timeout(TIMEOUT_LIMIT):
                self.connection.get_database(DB_NAME).user.update_one({"id": user_id}, {"$set": {"username": new_username}})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_UPDATE_USERNAME.value)

    def destroy_tokens(self, user_id: str) -> None:
        try:
            with timeout(TIMEOUT_LIMIT):
                self.connection.get_database(DB_NAME).expiring_token.delete_many({"userId": user_id})
        except Exception:
            raise Exception(ErrorCodes.FAILED_TO_DESTROY_TOKENS.value)
