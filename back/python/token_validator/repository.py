import os

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient, errors


load_dotenv()


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
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to get token! - {str(e)}")
        return item

