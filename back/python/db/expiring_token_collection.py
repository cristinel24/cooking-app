import pymongo.errors

from db.mongo_collection import MongoCollection


class ExpiringTokenCollection(MongoCollection):
    def __init__(self):
        super()
        self._collection = self._connection.cooking_app.expiring_token

    def get_expiring_token(self, token: str):
        try:
            item = self._collection.find_one({"value": token})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to retrieve user context! - {str(e)}")
        return item

    def insert_token(self, token: str, ):
        pass
