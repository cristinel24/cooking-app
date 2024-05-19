import pymongo.errors
from pymongo import MongoClient
from constants import *
from utils import match_collection_error


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URI)

    def get_connection(self) -> MongoClient:
        return self._connection


class ExpiringTokenCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.expiring_token

    def find_and_remove_token(self, value: str, session) -> dict | None:
        try:
            return self._collection.find_one_and_delete({"value": value}, session=session)
        except pymongo.errors.PyMongoError as e:
            raise match_collection_error(e)

    def find_and_remove_token_by_user_id(self, user_id: str, session) -> dict | None:
        try:
            self._collection.delete_many({"userId": user_id}, session=session)
        except pymongo.errors.PyMongoError as e:
            raise match_collection_error(e)
