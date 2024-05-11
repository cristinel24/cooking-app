import os
import pymongo
import constants
import exceptions


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(
            os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))


class TagCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.tag

    async def get_first_tags_starting_with(self, starting_with: str) -> list[str]:
        with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find(
                {"tag": {"$regex": f"^{starting_with}"}},
                limit=constants.NO_OF_RETURNED_ITEMS
            ).sort('counter', -1)

            return [item["tag"] for item in result]

    async def add_tag_by_name(self, name: str) -> None:
        with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find_one({"tag": name})

            if result:
                self._collection.update_one(result, {"$inc": {"counter": 1}})
            else:
                self._collection.insert_one({"tag": name, "counter": 1})

    async def remove_tag_by_name(self, name: str) -> None:
        with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find_one({"tag": name})

            if not result:
                raise exceptions.TagException(constants.ErrorCodes.NONEXISTENT_TAG.value)

            if result["counter"] == 1:
                self._collection.delete_one(result)
            else:
                self._collection.update_one(result, {"$inc": {"counter": -1}})
