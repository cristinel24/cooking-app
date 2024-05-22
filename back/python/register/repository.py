from pprint import pprint

import pymongo
from constants import MONGO_URI, DB_NAME, MONGO_TIMEOUT
from pymongo import MongoClient


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        db = self._connection.get_database(DB_NAME)
        self._collection = db.get_collection("user")

    def user_exists_by_field(self, attribute: str, value: str) -> bool:
        with pymongo.timeout(MONGO_TIMEOUT):
            return self._collection.find_one({attribute: value}) is not None

    async def insert_user(self, user_data: dict, empty_fields: dict) -> None:
        with pymongo.timeout(MONGO_TIMEOUT):
            new_user = {**user_data, **empty_fields}
            pprint(new_user)
            self._collection.insert_one(new_user)
