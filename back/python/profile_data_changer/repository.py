import pymongo
from pymongo import MongoClient, errors
from constants import MONGO_URL, DB_NAME, ErrorCodes, MONGO_TIMEOUT


class MongoCollection:
    def __init__(self, connection: MongoClient = None):
        self._collection = connection if connection is not None else MongoClient(MONGO_URL)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient = None):
        super().__init__(connection)
        db = self._collection.get_database(DB_NAME)
        self._collection = db.user

    def get_user_by_id(self, user_id: str) -> dict:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                user = self._collection.find({"id": user_id})
                if user is None:
                    raise Exception(ErrorCodes.USER_NOT_FOUND.value)
                return user
        except errors.PyMongoError:
            raise Exception(ErrorCodes.DATABASE_ERROR.value)

    def patch_user(self, user_id: str, changes: dict) -> None:
        try:
            if not self.get_user_by_id(user_id):
                raise Exception(ErrorCodes.USER_NOT_FOUND.value)
            with pymongo.timeout(MONGO_TIMEOUT):
                self._collection.update_one({"id": user_id}, {"$set": changes})
        except errors.PyMongoError:
            raise Exception(ErrorCodes.DATABASE_ERROR.value)

    def add_allergens(self, user_id: str, allergens_to_add: list[str]) -> None:
        try:
            if not self.get_user_by_id(user_id):
                raise Exception(ErrorCodes.USER_NOT_FOUND.value)
            with pymongo.timeout(MONGO_TIMEOUT):
                self._collection.update_one({"id": user_id}, {"$push": {"allergens": {"$each": allergens_to_add}}})
        except errors.PyMongoError:
            raise Exception(ErrorCodes.DATABASE_ERROR.value)

    def remove_allergens(self, user_id: str, allergens_to_remove: list[str]) -> None:
        try:
            if not self.get_user_by_id(user_id):
                raise Exception(ErrorCodes.USER_NOT_FOUND.value)
            with pymongo.timeout(MONGO_TIMEOUT):
                self._collection.update_one({"id": user_id}, {"$pull": {"allergens": {"$in": allergens_to_remove}}})
        except errors.PyMongoError:
            raise Exception(ErrorCodes.DATABASE_ERROR.value)
