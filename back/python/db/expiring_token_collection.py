from datetime import datetime
from bson import ObjectId

from db.mongo_collection import MongoCollection


class ExpiringTokenCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.cooking_app.expiring_token

    def get_expiring_token_by_value(self, value: str) -> dict:
        try:
            item = self._collection.find_one({"value": value})
        except Exception as e:
            raise Exception(f"Failed to get token! - {str(e)}")
        return item

    def remove_token(self, token_id: ObjectId):
        try:
            result = self._collection.delete_one({"_id": token_id})
            if result.deleted_count == 0:
                raise Exception(f"No tokens were removed")
        except Exception as e:
            raise Exception(f"Failed to remove token! - {str(e)}")

    def insert_token(self, value: str, user_id: ObjectId, type_token: str) -> int:
        """
        insert a new token in the db, return the inserted token's id
        :param value: token value
        :param user_id: token's user id
        :param type_token: token's type
        :return: ObjectId of the newly inserted token
        """
        try:
            item = self._collection.insert_one({
                "value": value,
                "createdAt": datetime.utcnow(),
                "userId": user_id,
                "type": type_token
            })
            return item.inserted_id
        except Exception as e:
            raise Exception(f"Failed to insert token! - {str(e)}")

#
# if __name__ == "__main__":
#     coll = ExpiringTokenCollection()
#     print(coll.insert_token("a7c6e4b3821299857824f9bc0c89d7a70714361b8dacd6e22a4240197fe69420", ObjectId("662bba36255bb1d5983c66db"), "session"))
