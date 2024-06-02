import pymongo
from constants import DB_NAME, MONGO_TIMEOUT, MONGO_URI, ErrorCodes
from exception import VerifierException
from fastapi import status
from pymongo import MongoClient, errors
from datetime import datetime, timezone


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        db = self._connection.get_database(DB_NAME)
        self._collection = db.user

    def update_user_by_id(self, user_id: str, pipeline: list[dict]) -> None:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                pipeline[0]["$match"]["id"] = user_id
                pipeline[1]["$set"]["updatedAt"] = datetime.now(timezone.utc)
                self._collection.aggregate(pipeline)
        except errors.PyMongoError as e:
            if e.timeout:
                raise VerifierException(status.HTTP_504_GATEWAY_TIMEOUT, ErrorCodes.DATABASE_TIMEOUT.value)
            else:
                raise VerifierException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR.value)
