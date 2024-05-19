import exceptions
import pymongo
from constants import *


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URI)


class TagCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).tag

    async def get_first_tags_starting_with(self, starting_with: str) -> list[str]:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find(
                {"tag": {"$regex": f"^{starting_with}"}},
                limit=NO_OF_RETURNED_ITEMS
            ).sort('counter', -1)

            return [item["tag"] for item in result]

    async def add_tag_by_name(self, name: str) -> None:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find_one({"tag": name})

            if result:
                self._collection.update_one(result, {"$inc": {"counter": 1}})
            else:
                self._collection.insert_one({"tag": name, "counter": 1})

    async def add_tags(self, names: list[str]) -> None:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            results = [result["tag"] for result in self._collection.find({"tag": {"$in": names}})]
            if results:
                self._collection.update_many({"tag": {"$in": results}}, {"$inc": {"counter": 1}})
            new_tags = [{"tag": tag, "counter": 1} for tag in names if tag not in results]
            if new_tags:
                self._collection.insert_many(new_tags)

    async def remove_tag_by_name(self, name: str) -> None:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find_one({"tag": name})

            if not result:
                raise exceptions.TagException(ErrorCodes.NONEXISTENT_TAG.value)

            if result["counter"] == 1:
                self._collection.delete_one(result)
            else:
                self._collection.update_one(result, {"$inc": {"counter": -1}})
                self._collection.update_one(result, {"$inc": {"counter": -1}})

    async def decrement_tags(self, names: list[str]) -> None:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            results = [(result["tag"], result["counter"]) for result in
                       self._collection.find({"tag": {"$in": names}})]
            deleted_tags = [tag for tag in results if tag[1] == 1]
            if deleted_tags:
                self._collection.delete_many(
                    {"tag": {"$in": [deleted_tag[0] for deleted_tag in deleted_tags]}})
                results.remove(*deleted_tags)
            if results:
                self._collection.update_many({"tag": {"$in": [result[0] for result in results]}},
                                             {"$inc": {"counter": -1}})
