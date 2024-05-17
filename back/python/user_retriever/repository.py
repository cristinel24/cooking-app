import pymongo
from pymongo import MongoClient, errors
from constants import MONGO_URL, DB_NAME, ErrorCodes, MONGO_TIMEOUT
from exception import UserRetrieverException
from fastapi import status


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URL)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        db = self._connection.get_database(DB_NAME)
        self._collection = db.user

    def get_user_by_id(self, user_id: str, projection_arg: dict) -> dict:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                user = self._collection.find_one({"id": user_id}, projection=projection_arg)
                if user is None:
                    raise UserRetrieverException(status.HTTP_status.HTTP_404_NOT_FOUND_NOT_FOUND, ErrorCodes.USER_NOT_FOUND)
                return user
        except errors.PyMongoError:
            raise UserRetrieverException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR)

    def get_users_by_id(self, user_ids: list[str], projection_arg: dict) -> list[dict]:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                users_list = list(self._collection.find({"id": {"$in": user_ids}}, projection=projection_arg))
                if not users_list:
                    raise UserRetrieverException(status.HTTP_404_NOT_FOUND, ErrorCodes.USER_NOT_FOUND)
                return users_list
        except errors.PyMongoError:
            raise UserRetrieverException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR)
