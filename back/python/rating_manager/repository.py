from datetime import datetime, timezone
from typing import Mapping, Any

import pymongo.errors
from fastapi import status
from pymongo import MongoClient, timeout, ReturnDocument
from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from pymongo.results import UpdateResult, DeleteResult

from constants import MONGO_URI, ErrorCodes, DB_NAME, NORMAL_TIMEOUT_DB, RATING_PROJECTION, LARGE_TIMEOUT_DB
from exception import RecipeRatingManagerException
from schemas import RatingCreate
from utils import transform_exception


def _update_entry_by_id(
        collection: Collection, entry_id: str, update: dict,
        session: ClientSession, error: ErrorCodes, status_code: int
) -> UpdateResult:
    try:
        with timeout(NORMAL_TIMEOUT_DB):
            update.update({"$set": {"updatedAt": datetime.now(timezone.utc)}})
            update = collection.update_one(
                filter={"id": entry_id},
                update=update,
                session=session
            )

            if update.matched_count == 0:
                raise RecipeRatingManagerException(
                    error_code=error, status_code=status_code
                )

            return update

    except Exception as e:
        raise transform_exception(e)


class MongoCollection:

    def __init__(self, connection: MongoClient | None = None):
        if connection is None:
            self._connection = MongoClient(MONGO_URI)
        else:
            self._connection = connection
        try:
            self._connection.admin.command("ping")
        except ConnectionError:
            raise RecipeRatingManagerException(
                ErrorCodes.DB_CONNECTION_FAILURE.value,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_connection(self) -> MongoClient:
        return self._connection


class RatingCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).get_collection("rating")

    def find_ratings(
            self, parent_id: str, start: int, count: int,
            filter_aggregate: dict, sort_aggregate: dict
    ) -> (int, list[dict]):

        try:
            with timeout(LARGE_TIMEOUT_DB):
                result = self._collection.aggregate(
                    pipeline=[{
                        "$facet": {
                            "data": [
                                {"$match": {"parentId": parent_id} | filter_aggregate},
                                {"$skip": start},
                                {"$limit": count},
                                {"$sort": sort_aggregate},
                                {"$project": RATING_PROJECTION}
                            ],
                            "total": [
                                {"$match": {"parentId": parent_id} | filter_aggregate},
                                {"$count": "total"}
                            ]
                        }
                    }]
                ).next()

                if len(result["data"]) == 0:
                    return 0, []

                return result["total"][0]["total"], result["data"]
        except Exception as e:
            raise transform_exception(e)

    def find_rating_by_id(self, rating_id) -> dict:
        try:
            with timeout(NORMAL_TIMEOUT_DB):
                return self._collection.find_one(filter={"id": rating_id}, projection=RATING_PROJECTION)

        except Exception as e:
            raise transform_exception(e)

    def find_rating_by_recipe_and_author_id(self, recipe_id: str, author_id: str) -> dict:
        try:
            with timeout(NORMAL_TIMEOUT_DB):
                rating: dict = self._collection.find_one(
                    filter={
                        "authorId": author_id,
                        "parentId": recipe_id,
                        "parentType": "recipe",
                    },
                    projection=RATING_PROJECTION
                )
                if not rating:
                    raise RecipeRatingManagerException(
                        error_code=ErrorCodes.RATING_NOT_FOUND,
                        status_code=status.HTTP_404_NOT_FOUND
                    )
                return rating

        except Exception as e:
            raise transform_exception(e)

    def update_rating(self, rating_id: str, update: dict, session: ClientSession = None) -> UpdateResult:
        return _update_entry_by_id(
            self._collection,
            rating_id,
            update,
            session,
            ErrorCodes.RATING_NOT_FOUND,
            status.HTTP_404_NOT_FOUND
        )

    def create_rating(
            self, user_id: str, generated_id: str, rating_data: RatingCreate, session: ClientSession = None
    ) -> None:

        try:
            with timeout(NORMAL_TIMEOUT_DB):
                self._collection.insert_one(
                    document={
                        "id": generated_id,
                        "updatedAt": datetime.now(timezone.utc),
                        "authorId": user_id,
                        "parentType": rating_data.parentType,
                        "parentId": rating_data.parentId,
                        "rating": rating_data.rating,
                        "description": rating_data.description,
                        "children": [],
                    },
                    session=session
                )

        except pymongo.errors.DuplicateKeyError as e:
            if "authorId_1_parentId_1" in str(e):
                raise RecipeRatingManagerException(
                    error_code=ErrorCodes.USER_ALREADY_COMMENTED, status_code=status.HTTP_403_FORBIDDEN
                )
            if "id_1" in str(e):
                raise RecipeRatingManagerException(
                    error_code=ErrorCodes.DUPLICATE_GENERATED_ID, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            raise RecipeRatingManagerException(
                error_code=ErrorCodes.UNKNOWN, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            raise transform_exception(e)

    def delete_rating(self, rating_id: str, session: ClientSession = None) -> DeleteResult:
        try:
            with timeout(NORMAL_TIMEOUT_DB):
                return self._collection.delete_one(
                    filter={"id": rating_id},
                    session=session
                )

        except Exception as e:
            raise transform_exception(e)

    def find_and_update_rating(self, rating_id: str, update: dict, session: ClientSession = None):
        try:
            with timeout(NORMAL_TIMEOUT_DB):
                update["$set"]["updatedAt"] = datetime.now(timezone.utc)
                rating = self._collection.find_one_and_update(
                    filter={"id": rating_id},
                    update=update,
                    return_document=ReturnDocument.AFTER,
                    projection=RATING_PROJECTION,
                    session=session,
                )
                if rating is None:
                    raise RecipeRatingManagerException(
                        error_code=ErrorCodes.PARENT_RATING_NOT_FOUND,
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                return rating

        except Exception as e:
            raise transform_exception(e)

    def get_children(self, filter: dict):
        try:
            with timeout(10):
                all_children: list[(str, str)] = []
                for projection in self._collection.find(
                        filter=filter, projection={
                            "_id": 0, "authorId": 1, "id": 1
                        }
                ):
                    all_children.append((projection["authorId"], projection["id"]))

                return all_children

        except Exception as e:
            raise transform_exception(e)

    def delete_many(self, ids: list[str], session: ClientSession = None):
        try:
            with timeout(10):
                self._collection.delete_many(filter={"id": {"$in": ids}}, session=session)

        except Exception as e:
            raise transform_exception(e)


class RecipeCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).get_collection("recipe")

    def find_recipe(self, recipe_id: str):
        try:
            with timeout(NORMAL_TIMEOUT_DB):
                return self._collection.find_one({"id": recipe_id})

        except Exception as e:
            raise transform_exception(e)

    def modify_recipe(self, recipe_id: str, mods: dict, session: ClientSession = None):
        try:
            with timeout(NORMAL_TIMEOUT_DB):
                mods.update({"$set": {"updatedAt": datetime.now(timezone.utc)}})
                self._collection.update_one(
                    filter={"id": recipe_id},
                    update=mods,
                    session=session
                )

        except Exception as e:
            raise transform_exception(e)


class UserCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).get_collection("user")

    def update_user(
            self, author_id: str, update: dict, session: ClientSession = None
    ) -> UpdateResult:
        return _update_entry_by_id(
            self._collection,
            author_id,
            update,
            session,
            ErrorCodes.AUTHOR_NOT_FOUND,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def remove_ratings_from_many(self, authors: list[str], ratings: list[str]):
        try:
            with timeout(NORMAL_TIMEOUT_DB):
                self._collection.update_many(
                    filter={"id": {"$in": authors}},
                    update={"$pull": {"ratings": {"$in": ratings}}}
                )

        except Exception as e:
            raise transform_exception(e)
