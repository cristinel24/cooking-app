import os
from datetime import datetime

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient, errors
from schemas import expiring_token_projection


load_dotenv()


class TokenCollection:
    def __init__(self):
        self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
        self._collection = self._connection.cooking_app.expiring_token

    def insert_token(self, value: str, user_id: str, type_token: str) -> dict:
        try:
            item = self._collection.insert_one({
                "value": value,
                "createdAt": datetime.utcnow(),
                "userId": user_id,
                "tokenType": type_token
            })
            item = self._collection.find_one({"_id": item.inserted_id}, projection=expiring_token_projection)
            print(item)
            return item
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to insert token! - {str(e)}")


