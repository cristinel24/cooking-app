import pymongo.errors
from pymongo import MongoClient

from db.mongo_collection import MongoCollection


class CountersCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.counters

    def get_name_incrementor_value(self) -> int:
        try:
            result = self._collection.find_one_and_update(
                {'type': "nameIncrementor"},
                {'$inc': {'value': 1}}
            )
            return result["value"]
        except pymongo.errors.PyMongoError as e:
            print(e)
