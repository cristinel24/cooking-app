import pymongo.errors
from pymongo import MongoClient
from constants import *
from utils import match_collection_error


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URI)

    def get_connection(self) -> MongoClient:
        return self._connection


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def exists_user(self, user_id: str):
        try:
            return self._collection.find_one({"id": user_id}) is not None
        except pymongo.errors.PyMongoError as e:
            raise match_collection_error(e)



class ExpiringTokenCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).expiring_token

    def find_and_remove_token(self, value: str) -> dict | None:
        try:
            return self._collection.find_one_and_delete({"value": value})
        except pymongo.errors.PyMongoError as e:
            raise match_collection_error(e)

    def find_and_remove_token_by_user_id(self, user_id: str) -> dict | None:
        try:
            self._collection.delete_many({"userId": user_id})
        except pymongo.errors.PyMongoError as e:
            raise match_collection_error(e)
