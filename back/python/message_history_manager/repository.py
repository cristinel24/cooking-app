import pymongo
from constants import MONGO_URL

import constants


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URL)


class MessageHistoryCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def get_message_history(self, user_id: str, start: int, count: int) -> list[str]:
        with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.find_one(
                {"id": user_id},
                {"messageHistory": {"$slice": [start, count]}}
            )
        return result["messageHistory"] if result else []

    def add_message_history(self, user_id: str, message: str):
        with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
            update_result = self._collection.update_one(
                {"id": user_id},
                {"$push": {"messageHistory": message}}
            )
        return update_result.modified_count > 0

    def clear_message_history(self, user_id: str):
        update_result = self._collection.update_one(
            {"id": user_id},
            {"$set": {"messageHistory": []}}
        )
        return update_result.modified_count > 0
