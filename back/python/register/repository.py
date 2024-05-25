import pymongo
from constants import MONGO_URI, DB_NAME, MONGO_TIMEOUT
from pymongo import MongoClient


class MongoCollection:
    def __init__(self, connection: MongoClient = None):
        self.connection = connection if connection is not None else MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient = None):
        super().__init__(connection)
        db = self.connection.get_database(DB_NAME)
        self._collection = db.user

    def user_exists_by_fields(self, fields: list) -> dict:
        with pymongo.timeout(MONGO_TIMEOUT):
            return self._collection.find_one({"$or": fields})

    def insert_user(self, user_data: dict, empty_fields: dict) -> None:
        with pymongo.timeout(MONGO_TIMEOUT):
            new_user = {**user_data, **empty_fields}
            self._collection.insert_one(new_user)
