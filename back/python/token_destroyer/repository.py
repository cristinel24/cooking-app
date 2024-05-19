import pymongo.errors
from pymongo import MongoClient
from constants import *
from exception import TokenDestroyerException
from utils import match_collection_error
from fastapi import status


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
            with pymongo.timeout(MAX_TIMEOUT):
                return self._collection.find_one({"id": user_id}) is not None
        except pymongo.errors.PyMongoError as e:
            raise match_collection_error(e)



class ExpiringTokenCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).expiring_token

    def find_and_remove_token(self, value: str):
        try:
            with pymongo.timeout(MAX_TIMEOUT):
                res = self._collection.delete_one({"value": value})

                if res.deleted_count == 0:
                    raise TokenDestroyerException(status.HTTP_404_NOT_FOUND, ErrorCodes.TOKEN_NOT_FOUND.value)
        except pymongo.errors.PyMongoError as e:
            raise match_collection_error(e)

    def find_and_remove_token_by_user_id(self, user_id: str) -> dict | None:
        try:
            with pymongo.timeout(MAX_TIMEOUT):
                self._collection.delete_many({"userId": user_id})
        except pymongo.errors.PyMongoError as e:
            raise match_collection_error(e)
