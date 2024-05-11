from pymongo import MongoClient, errors
from constants import MONGO_URL, DB_NAME, ErrorCodes


class MongoCollection:
    def __init__(self, connection: MongoClient = None):
        self._collection = connection if connection is not None else MongoClient(MONGO_URL)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient = None):
        super().__init__(connection)
        db = self._collection.get_database(DB_NAME)
        self._collection = db.user

    def get_user(self, user_id: int) -> dict | None:
        try:
            print(self._collection.find_one({"id": user_id}))
            return self._collection.find_one({"id": user_id})
        except errors.PyMongoError:
            raise Exception(ErrorCodes.DATABASE_ERROR.value)

    def patch_user(self, user_id: int, changes: dict) -> None:
        try:
            if not self.get_user(user_id):
                raise Exception(ErrorCodes.USER_NOT_FOUND.value)
            self._collection.update_one({"user_id": user_id}, {"$set": changes})
        except errors.PyMongoError:
            raise Exception(ErrorCodes.DATABASE_ERROR.value)

    def add_allergens(self, user_id, allergens_to_add) -> None:
        try:
            if not self.get_user(user_id):
                raise Exception(ErrorCodes.USER_NOT_FOUND.value)
            self._collection.update_one({"user_id": user_id}, {"$push": {"allergens": {"$each": allergens_to_add}}})
        except errors.PyMongoError:
            raise Exception(ErrorCodes.DATABASE_ERROR.value)

    def remove_allergens(self, user_id, allergens_to_remove) -> None:
        try:
            if not self.get_user(user_id):
                raise Exception(ErrorCodes.USER_NOT_FOUND.value)
            self._collection.update_one({"user_id": user_id}, {"$pull": {"allergens": {"$in": allergens_to_remove}}})
        except errors.PyMongoError:
            raise Exception(ErrorCodes.DATABASE_ERROR.value)
