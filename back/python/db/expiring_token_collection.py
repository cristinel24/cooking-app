from datetime import datetime

import pymongo.errors
from bson import ObjectId

from db.mongo_collection import MongoCollection


class ExpiringTokenCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.cooking_app.expiring_token

    def get_expiring_token(self, token: str):
        try:
            item = self._collection.find_one({"value": token})
        # TODO: exception handling
        except Exception as e:
            raise Exception(f"Failed to retrieve user context! - {str(e)}")
        return item

    def insert_token(self, token: str, user_id: ObjectId, type_token: str):
        try:
            item = self._collection.insert_one({
                "value": token,
                "createdAt": datetime.utcnow(),
                "userId": user_id,
                "type": type_token
            })
            return item.inserted_id
        except Exception as e:
            raise Exception(f"Failed to insert token! - {str(e)}")
        pass

#
# if __name__ == "__main__":
#     coll = ExpiringTokenCollection()
#     print(coll.insert_token("a7c6e4b3821299857824f9bc0c89d7a70714361b8dacd6e22a4240197fe69420", ObjectId("662bba36255bb1d5983c66db"), "session"))
