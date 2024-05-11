from pymongo import MongoClient, errors

from constants import MONGO_URL


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URL)


class SearchHistoryCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def get_search_history(self, user_id: str, start: int, count: int) -> list[str]:
        try:
            result = self._collection.find_one(
                {"id": user_id},
                {"searchHistory": {"$slice": [start, count]}}
            )
            return result["searchHistory"] if result else []
        except errors.PyMongoError as e:
            raise Exception(f"Error while getting search history: {e}")

    def add_search_history(self, user_id: str, search_query: str):
        try:
            update_result = self._collection.update_one(
                {"id": user_id},
                {"$push": {
                    "searchHistory": {
                        "$each": [search_query],
                        "$slice": -100  # Keeps only the last 100 entries
                    }
                }}
            )
            return "Search history updated successfully" if update_result.modified_count > 0 else []
        except errors.PyMongoError as e:
            raise Exception(f"Error while adding search history: {str(e)}")

    def clear_search_history(self, user_id: str):
        try:
            update_result = self._collection.update_one(
                {"id": user_id},
                {"$set": {"searchHistory": []}}
            )
            return "Search history cleared successfully" if update_result.modified_count > 0 else []
        except errors.PyMongoError as e:
            raise Exception(f"Error while clearing search history: {str(e)}")
