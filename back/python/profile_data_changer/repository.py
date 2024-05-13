import pymongo
from pymongo import MongoClient, errors
from constants import MONGO_URL, DB_NAME, ErrorCodes, MONGO_TIMEOUT
from exception import ProfileDataChangerException
from fastapi import status


class MongoCollection:
    def __init__(self, connection: MongoClient = None):
        self.connection = connection if connection is not None else MongoClient(MONGO_URL)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient = None):
        super().__init__(connection)
        db = self.connection.get_database(DB_NAME)
        self._collection = db.user

    def patch_user(self, user_id: str, changes: dict) -> None:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                updated = self._collection.update_one({"id": user_id}, {"$set": changes})
            if updated.modified_count == 0:
                raise ProfileDataChangerException(HTTP_404_NOT_FOUND, ErrorCodes.USER_NOT_FOUND.value)
        except errors.PyMongoError:
            raise ProfileDataChangerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR.value)

    def add_allergens(self, user_id: str, allergens_to_add: list[str]) -> None:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                updated = self._collection.update_one({"id": user_id},
                                                      {"$push": {"allergens": {"$each": allergens_to_add}}})
                if updated.modified_count == 0:
                    raise ProfileDataChangerException(status.HTTP_404_NOT_FOUND, ErrorCodes.INVALID_DATA.value)
        except errors.PyMongoError:
            raise ProfileDataChangerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR.value)

    def remove_allergens(self, user_id: str, allergens_to_remove: list[str]) -> None:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                updated = self._collection.update_one({"id": user_id},
                                                      {"$pull": {"allergens": {"$in": allergens_to_remove}}})
                if updated.modified_count == 0:
                    raise ProfileDataChangerException(status.HTTP_404_NOT_FOUND, ErrorCodes.INVALID_DATA.value)
        except errors.PyMongoError:
            raise ProfileDataChangerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR.value)
