import pymongo
from pymongo import MongoClient, errors
from pymongo.errors import NetworkTimeout

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
                user = self._collection.find_one({"id": user_id})
                if user is None:
                    raise exceptions.SearchHistoryException(constants.ErrorCodes.USER_NOT_FOUND, 404)
                result = self._collection.find_one(
                    {"id": user_id},
                    {"searchHistory": {"$slice": [start, count]}}
                )
            search_history = result["searchHistory"] if result and "searchHistory" in result else []
            return search_history
        except errors.PyMongoError:
            raise exceptions.SearchHistoryException(constants.ErrorCodes.DB_CONNECTION_FAILURE, 500)
        except NetworkTimeout:
            raise exceptions.SearchHistoryException(constants.ErrorCodes.DB_CONNECTION_TIMEOUT, 504)

    def add_search_history(self, user_id: str, search_query: str):
        try:
            with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
                user = self._collection.find_one({"id": user_id})
                if user is None:
                    raise exceptions.SearchHistoryException(constants.ErrorCodes.USER_NOT_FOUND, 404)
                update_result = self._collection.update_one(
                    {"id": user_id},
                    {"$push": {
                        "searchHistory": {
                            "$each": [search_query],
                            "$slice": -100  # Keeps only the last 100 entries
                        }
                    }}
                )
            return True if update_result.modified_count > 0 else False
        except errors.PyMongoError:
            raise exceptions.SearchHistoryException(constants.ErrorCodes.DB_CONNECTION_FAILURE, 500)
        except NetworkTimeout:
            raise exceptions.SearchHistoryException(constants.ErrorCodes.DB_CONNECTION_TIMEOUT, 504)

    def clear_search_history(self, user_id: str):
        try:
            with pymongo.timeout(constants.MAX_TIMEOUT_TIME_SECONDS):
                user = self._collection.find_one({"id": user_id})
                if user is None:
                    raise exceptions.SearchHistoryException(constants.ErrorCodes.USER_NOT_FOUND, 404)
                update_result = self._collection.update_one(
                    {"id": user_id},
                    {"$set": {"searchHistory": []}}
                )
            return True if update_result.modified_count > 0 else False
        except errors.PyMongoError:
            raise exceptions.SearchHistoryException(constants.ErrorCodes.DB_CONNECTION_FAILURE, 500)
        except NetworkTimeout:
            raise exceptions.SearchHistoryException(constants.ErrorCodes.DB_CONNECTION_TIMEOUT, 504)
