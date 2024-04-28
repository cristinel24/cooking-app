from datetime import datetime
from bson import ObjectId
import pymongo.errors

from db.mongo_collection import MongoCollection


class ExpiringTokenCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.cooking_app.expiring_token

    def get_expiring_token_by_value(self, value: str) -> dict:
        try:
            item = self._collection.find_one({
                "value": value
            })
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to get token! - {str(e)}")
        return item

    def get_expiring_token_by_value_and_type(self, value: str, token_type: str) -> dict:
        try:
            item = self._collection.find_one({
                "value": value,
                "type": token_type
            })
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to get token! - {str(e)}")
        return item

    def remove_token(self, token_id: ObjectId):
        try:
            result = self._collection.delete_one({"_id": token_id})
            if result.deleted_count == 0:
                raise Exception(f"No tokens were removed")
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to remove token! - {str(e)}")

    def insert_token(self, value: str, user_id: ObjectId, type_token: str) -> str:
        """
        insert a new token in the db, return the inserted token's id
        :param value: token value
        :param user_id: token's user id
        :param type_token: token's type
        :return: id of the newly inserted token, as str (must be manually cast to ObjectId)
        """
        try:
            item = self._collection.insert_one({
                "value": value,
                "createdAt": datetime.utcnow(),
                "userId": user_id,
                "type": type_token
            })
            return str(item.inserted_id)
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to insert token! - {str(e)}")
