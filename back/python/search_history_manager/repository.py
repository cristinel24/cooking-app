import pymongo
from fastapi import status
from pymongo import MongoClient, errors

import exceptions
from constants import *
from utils import match_collection_error


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URI)


class SearchHistoryCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def get_search_history(self, user_id: str, start: int, count: int) -> list[str]:
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                result = self._collection.find_one(
                    {"id": user_id},
                    {"searchHistory": {"$slice": [-start - count, count]}}
                )
            if result is None:
                raise exceptions.SearchHistoryException(ErrorCodes.USER_NOT_FOUND, status.HTTP_404_NOT_FOUND)
            return result["searchHistory"]
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def add_search_history(self, user_id: str, search_query: str):
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                update_result = self._collection.update_one(
                    {"id": user_id},
                    {"$push": {
                        "searchHistory": {
                            "$each": [search_query],
                            "$slice": -HISTORY_MAX_SIZE  # Keeps only the last 100 entries
                        }
                    }}
                )
            if update_result.modified_count == 0:
                raise exceptions.SearchHistoryException(ErrorCodes.USER_NOT_FOUND, status.HTTP_404_NOT_FOUND)
            return update_result.modified_count
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def clear_search_history(self, user_id: str):
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                update_result = self._collection.update_one(
                    {"id": user_id},
                    {"$set": {"searchHistory": []}}
                )
            return update_result.modified_count
        except errors.PyMongoError as e:
            raise match_collection_error(e)
