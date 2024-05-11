import logging
from pymongo import MongoClient, errors
from constants import MONGO_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URL)


class MessageHistoryCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def get_message_history(self, user_id: str, start: int, count: int) -> list[str]:
        try:
            result = self._collection.find_one(
                {"id": user_id},
                {"messageHistory": {"$slice": [start, count]}}
            )
            return result["messageHistory"] if result else []
        except errors.PyMongoError as e:
            logger.error(f"Error while getting message history: {e}")
            raise Exception(f"Error while getting message history: {e}")

    def add_message_history(self, user_id: str, message: str):
        try:
            update_result = self._collection.update_one(
                {"id": user_id},
                {"$push": {"messageHistory": message}}
            )
            return update_result.modified_count > 0
        except errors.PyMongoError as e:
            logger.error(f"Error while adding message history: {e}")
            raise Exception(f"Error while adding message history: {e}")

    def clear_message_history(self, user_id: str):
        try:
            update_result = self._collection.update_one(
                {"id": user_id},
                {"$set": {"messageHistory": []}}
            )
            return update_result.modified_count > 0
        except errors.PyMongoError as e:
            logger.error(f"Error while clearing message history: {e}")
            raise Exception(f"Error while clearing message history: {e}")
