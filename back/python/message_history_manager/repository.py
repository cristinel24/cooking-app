import pymongo
from pymongo import errors
from pymongo.errors import NetworkTimeout

import constants
import exceptions


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(constants.MONGO_URL)


class MessageHistoryCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def get_message_history(self, user_id: str, start: int, count: int) -> list[str]:
        try:
            with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
                user = self._collection.find_one({"id": user_id})
                if user is None:
                    raise exceptions.MessageHistoryException(constants.ErrorCodes.USER_NOT_FOUND, 404)
                result = self._collection.find_one(
                    {"id": user_id},
                    {"messageHistory": {"$slice": [start, count]}}
                )
            return result["messageHistory"] if result else []
        except errors.PyMongoError:
            raise exceptions.MessageHistoryException(constants.ErrorCodes.DB_CONNECTION_FAILURE, 500)
        except NetworkTimeout:
            raise exceptions.MessageHistoryException(constants.ErrorCodes.DB_CONNECTION_TIMEOUT, 504)

    def add_message_history(self, user_id: str, message: str):
        try:
            with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
                user = self._collection.find_one({"id": user_id})
                if user is None:
                    raise exceptions.MessageHistoryException(constants.ErrorCodes.USER_NOT_FOUND, 404)
                update_result = self._collection.update_one(
                    {"id": user_id},
                    {"$push": {"messageHistory": message}}
                )
            return update_result.modified_count > 0
        except errors.PyMongoError:
            raise exceptions.MessageHistoryException(constants.ErrorCodes.DB_CONNECTION_FAILURE, 500)
        except NetworkTimeout:
            raise exceptions.MessageHistoryException(constants.ErrorCodes.DB_CONNECTION_TIMEOUT, 504)

    def clear_message_history(self, user_id: str):
        try:
            with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
                user = self._collection.find_one({"id": user_id})
                if user is None:
                    raise exceptions.MessageHistoryException(constants.ErrorCodes.USER_NOT_FOUND, 404)
            update_result = self._collection.update_one(
                {"id": user_id},
                {"$set": {"messageHistory": []}}
            )
            return update_result.modified_count > 0
        except errors.PyMongoError:
            raise exceptions.MessageHistoryException(constants.ErrorCodes.DB_CONNECTION_FAILURE, 500)
        except NetworkTimeout:
            raise exceptions.MessageHistoryException(constants.ErrorCodes.DB_CONNECTION_TIMEOUT, 504)
