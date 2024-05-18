from constants import *
from exception import UserDestroyerException
from pymongo import MongoClient, errors, timeout
from pymongo.client_session import ClientSession
from utils import match_collection_error


class MongoCollection:
    _connection = None

    def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(MONGO_URI)
        try:
            self._connection.admin.command('ping')
        except ConnectionError:
            raise UserDestroyerException(ErrorCodes.DB_CONNECTION_FAILURE, 500)

    def get_connection(self) -> MongoClient:
        return self._connection


class FollowCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).follow

    def delete_follows_by_user_id(self, user_id: str, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.delete_many({"$or": [{"userId": user_id},
                                                      {"followsId": user_id}]}, session=session)
        except errors.PyMongoError as e:
            raise match_collection_error(e)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def delete_user_by_user_id(self, user_id: str, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.delete_one({"id": user_id}, session=session)
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def ping_user(self, user_id: str):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                if self._collection.find_one({"id": user_id}, {"_id": 0, "id": 1}) is not None:
                    return True
        except errors.PyMongoError as e:
            raise match_collection_error(e)
        return False


class RecipeCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).recipe

    def update_author_id_by_user_id(self, user_id: str, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.update_many(
                    {"authorId": user_id},
                    {"$set": {"authorId": DELETED_USER_ID}},
                    session=session
                )
        except errors.PyMongoError as e:
            raise match_collection_error(e)


class RatingCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).rating

    def update_author_id_by_user_id(self, user_id: str, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.update_many(
                    {"authorId": user_id},
                    {"$set": {"authorId": DELETED_USER_ID}},
                    session=session
                )
        except errors.PyMongoError as e:
            raise match_collection_error(e)


class ReportCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).report

    def update_author_id_by_user_id(self, user_id: str, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.update_many(
                    {"authorId": user_id},
                    {"$set": {"authorId": DELETED_USER_ID}},
                    session=session
                )
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def delete_reported_id_by_user_id(self, user_id: str, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.delete_many(
                    {"reportedId": user_id},
                    session=session
                )
        except errors.PyMongoError as e:
            raise match_collection_error(e)


class ExpiringTokenCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).expiring_token

    def delete_expiring_tokens_by_user_id(self, user_id: str, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.delete_many({"userId": user_id}, session=session)
        except errors.PyMongoError as e:
            raise match_collection_error(e)
