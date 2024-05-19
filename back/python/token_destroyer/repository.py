import pymongo.errors
from pymongo import MongoClient
from constants import *
from utils import match_collection_error
from exception import TokenDestroyerException

class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URI)

    def get_connection(self) -> MongoClient:
        return self._connection

class ExpiringTokenCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.expiring_token

    def find_and_remove_token(self, value: str, session) -> dict:
        try:
            token_data = self._collection.find_one_and_delete({"value": value}, session=session)
            if not token_data:
                raise TokenDestroyerException(ErrorCodes.TOKEN_NOT_FOUND, 404)
            return token_data
        except pymongo.errors.PyMongoError as e:
            raise match_collection_error(e)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def update_user_field(self, user_id: str, field: str, value: str, session):
        """
        update only for sessions and login.changeToken fields in user
        """
        try:
            if field == "sessions":
                updated_items = self._collection.update_one(
                    {"id": user_id},
                    {"$pull": {field: {"value": value}}},
                    session=session)
            else:
                updated_items = self._collection.update_one(
                    {"id": user_id},
                    {"$set": {field: None}},
                    session=session)
            if updated_items.matched_count == 0:
                raise TokenDestroyerException(ErrorCodes.NO_USERS_MATCHED, 404)
            if updated_items.modified_count == 0:
                raise TokenDestroyerException(ErrorCodes.FAILED_TO_UPDATE_USER, 500)
        except pymongo.errors.PyMongoError as e:
            raise match_collection_error(e)

