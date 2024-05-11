import os

import pymongo
from constants import Errors
from pymongo import MongoClient, errors


class TokenCollection:
    def __init__(self):
        self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
        self._collection = self._connection.cooking_app.expiring_token

    def get_expiring_token(self, value: str, token_type: str | None = None) -> dict:
        try:
            find_query = {
                "value": value
            }
            if token_type is not None:
                find_query["tokenType"] = token_type
            item = self._collection.find_one(find_query)
            return item
        except pymongo.errors.ExecutionTimeout:
            return {"error_code": Errors.DB_TIMEOUT}
        except pymongo.errors.PyMongoError:
            return {"error_code": Errors.DB_ERROR}

