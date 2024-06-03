import pymongo
from pymongo import MongoClient, errors, ReturnDocument
from pymongo.client_session import ClientSession
from constants import MONGO_URI, DB_NAME, ErrorCodes, MONGO_TIMEOUT
from exception import ProfileDataChangerException
from fastapi import status
from utils import match_collection_error
from datetime import datetime, timezone


class MongoCollection:
    def __init__(self, connection: MongoClient = None):
        self.connection = connection if connection is not None else MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient = None):
        super().__init__(connection)
        db = self.connection.get_database(DB_NAME)
        self._collection = db.user

    def patch_user_and_get_allergens(self, user_id: str, changes: dict, session: ClientSession) -> set[str]:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                changes["$set"]["updatedAt"] = datetime.now(timezone.utc)
                updated_user = self._collection.find_one_and_update(
                    filter={"id": user_id},
                    update=changes,
                    return_document=ReturnDocument.BEFORE,
                    projection={"_id": 0, "allergens": 1},
                    session=session
                )
    
                if not updated_user:
                    raise ProfileDataChangerException(status.HTTP_404_NOT_FOUND, ErrorCodes.USER_NOT_FOUND.value)
                return set(updated_user["allergens"])
        except errors.PyMongoError as e:
            match_collection_error(e)
