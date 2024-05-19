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

    async def add_allergens(self, names: list[str]) -> None:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            results = [result["allergen"] for result in self._collection.find({"allergen": {"$in": names}})]
            if results:
                self._collection.update_many({"allergen": {"$in": results}}, {"$inc": {"counter": 1}})
            new_allergens = [{"allergen": allergen, "counter": 1} for allergen in names if allergen not in results]
            if new_allergens:
                self._collection.insert_many(new_allergens)

    async def remove_allergen_by_name(self, name: str) -> None:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find_one({"allergen": name})

            if not result:
                raise exceptions.AllergenException(ErrorCodes.NONEXISTENT_ALLERGEN.value)

            if result["counter"] == 1:
                self._collection.delete_one(result)
            else:
                self._collection.update_one(result, {"$inc": {"counter": -1}})

    async def decrement_allergens(self, names: list[str]) -> None:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            results = [(result["allergen"], result["counter"]) for result in
                       self._collection.find({"allergen": {"$in": names}})]
            deleted_allergens = [allergen for allergen in results if allergen[1] == 1]
            if deleted_allergens:
                self._collection.delete_many(
                    {"allergen": {"$in": [deleted_allergen[0] for deleted_allergen in deleted_allergens]}})
                results.remove(*deleted_allergens)
            if results:
                self._collection.update_many({"allergen": {"$in": [result[0] for result in results]}},
                                             {"$inc": {"counter": -1}})
