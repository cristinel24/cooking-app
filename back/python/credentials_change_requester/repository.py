import pymongo
from constants import DB_NAME, MONGO_TIMEOUT, MONGO_URI, ErrorCodes
from exceptions import CredentialChangeRequesterException
from fastapi import status
from pymongo import MongoClient, errors


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        db = self._connection.get_database(DB_NAME)
        self._collection = db.user

    def get_user_by_email(self, email: str, projection_arg: dict) -> dict:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                user = self._collection.find_one({"email": email}, projection=projection_arg)
                if user is None:
                    raise CredentialChangeRequesterException(status.HTTP_404_NOT_FOUND, ErrorCodes.USER_NOT_FOUND)
                return user
        except errors.PyMongoError:
            raise CredentialChangeRequesterException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR)
