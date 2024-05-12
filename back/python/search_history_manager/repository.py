import pymongo
from pymongo import MongoClient, errors
from utils import match_collection_error

import constants
import exceptions


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(constants.MONGO_URL)


class SearchHistoryCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def get_search_history(self, user_id: str, start: int, count: int) -> list[str]:
        try:
            with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
                result = self._collection.find_one(
                    {"id": user_id},
                    {"searchHistory": {"$slice": [start, count]}}
                )
            if result is None:
                raise exceptions.SearchHistoryException(constants.ErrorCodes.USER_NOT_FOUND, 404)
            return result["searchHistory"]
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def add_search_history(self, user_id: str, search_query: str):
        try:
            with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
                update_result = self._collection.update_one(
                    {"id": user_id},
                    {"$push": {
                        "searchHistory": {
                            "$each": [search_query],
                            "$slice": -100  # Keeps only the last 100 entries
                        }
                    }}
                )
            if update_result.modified_count == 0:
                raise exceptions.SearchHistoryException(constants.ErrorCodes.USER_NOT_FOUND, 404)
            return update_result.modified_count
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def clear_search_history(self, user_id: str):
        try:
            with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
                update_result = self._collection.update_one(
                    {"id": user_id},
                    {"$set": {"searchHistory": []}}
                )
            return update_result.modified_count
        except errors.PyMongoError as e:
            raise match_collection_error(e)
