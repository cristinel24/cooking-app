import pymongo
from constants import MONGO_URI, DB_NAME, MAX_TIMEOUT_TIME_SECONDS, NO_OF_RETURNED_ITEMS, ErrorCodes
import exceptions


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(
            MONGO_URI)


class AllergenCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).allergen

    async def get_first_allergens_starting_with(self, starting_with: str) -> list[str]:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find(
                {"allergen": {"$regex": f"^{starting_with}"}},
                limit=NO_OF_RETURNED_ITEMS
            ).sort('counter', -1)

            return [item["allergen"] for item in result]

    async def add_allergen_by_name(self, name: str) -> None:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find_one({"allergen": name})

            if result:
                self._collection.update_one(result, {"$inc": {"counter": 1}})
            else:
                self._collection.insert_one({"allergen": name, "counter": 1})

    async def remove_allergen_by_name(self, name: str) -> None:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find_one({"allergen": name})

            if not result:
                raise exceptions.AllergenException(ErrorCodes.NONEXISTENT_ALLERGEN.value)

            if result["counter"] == 1:
                self._collection.delete_one(result)
            else:
                self._collection.update_one(result, {"$inc": {"counter": -1}})
