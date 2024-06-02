import pymongo
from fastapi import status
from pymongo import errors
from datetime import datetime, timezone


import exceptions
from constants import (DB_NAME, HISTORY_MAX_SIZE, MAX_TIMEOUT_TIME_SECONDS,
                       MONGO_URI, ErrorCodes)
from utils import match_collection_error


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URI)


class MessageHistoryCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def get_message_history(self, user_id: str, start: int, count: int) -> list[str]:
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                result = self._collection.find_one(
                    {"id": user_id},
                    {"messageHistory": {"$slice": [-start - count, count]}}
                )
            if result is None:
                raise exceptions.MessageHistoryException(ErrorCodes.MESSAGE_HISTORY_NOT_FOUND,
                                                         status.HTTP_404_NOT_FOUND)
            return result["messageHistory"]
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def add_message_history(self, user_id: str, message: str):
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                update_result = self._collection.update_one(
                    {"id": user_id},
                    {"$push": {
                        "messageHistory": {
                            "$each": [message],
                            "$slice": -HISTORY_MAX_SIZE  # Keeps only the last 100 entries
                        }
                    },
                    "$set": {"updatedAt": datetime.now(timezone.utc)}
                    }
                )
            if update_result.modified_count == 0:
                raise exceptions.MessageHistoryException(ErrorCodes.USER_NOT_FOUND, status.HTTP_404_NOT_FOUND)
            return update_result.modified_count
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def clear_message_history(self, user_id: str):
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                update_result = self._collection.update_one(
                    {"id": user_id},
                    {"$set": {"messageHistory": []}}
                )
            if update_result.modified_count == 0:
                raise exceptions.MessageHistoryException(ErrorCodes.USER_NOT_FOUND, status.HTTP_404_NOT_FOUND)
            return update_result.modified_count
        except errors.PyMongoError as e:
            raise match_collection_error(e)
