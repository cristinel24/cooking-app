import asyncio

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from schemas import Rating, RatingUpdate
from constants import MONGO_URI, DB_NAME, MONGO_COLLECTION, RATING_PROJECTION, DELETED_FIELD
from exceptions import DatabaseError, InternalError, DatabaseNotFoundDataError
from utils import singleton, init_logger

OPERATION_TIMEOUT: int = 10
OPERATION_TIMEOUT_MESSAGE: str = "Database operation timed out"


@singleton
class RatingRepository:
    def __init__(self, db_url: str = MONGO_URI,
                 db_name: str = DB_NAME,
                 collection_name: str = MONGO_COLLECTION):
        self.client = AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.logger = init_logger("[REPOSITORY]")

    async def get_ratings_of_parent(self, parent_id: str, start: int, count: int) -> (dict, int):
        try:
            pipeline = [
                {"$match": {"parentId": parent_id}},
                {"$sort": {"updatedAt": 1}},
                {"$skip": start},
                {"$limit": count},
                {"$project": RATING_PROJECTION}
            ]

            cursor = self.collection.aggregate(pipeline, allowDiskUse=True)
            ratings = await asyncio.wait_for(cursor.to_list(length=count), timeout=OPERATION_TIMEOUT)
            if not ratings:
                return ratings, 0

            for rating in ratings:
                rating__id = ObjectId(rating["_id"])
                rating["createdAt"] = rating__id.generation_time
                rating.pop("_id")

            total_pipeline = [{"$match": {"parentId": parent_id}}, {"$count": "total"}]
            total_result = await asyncio.wait_for(self.collection.aggregate(total_pipeline).next(),
                                                  timeout=OPERATION_TIMEOUT)

            total = total_result.get("total", 0)

            return ratings, total

        except asyncio.TimeoutError:
            self.logger.error(OPERATION_TIMEOUT_MESSAGE)
            raise DatabaseError()
        except Exception as e:
            self.logger.error(e)
            raise InternalError()

    async def update_rating(self, rating_id: str, update: RatingUpdate):
        try:
            query = {"id": rating_id}
            rating = await asyncio.wait_for(
                self.collection.find_one_and_update(query, {"$set": {"description": update.description}}),
                timeout=OPERATION_TIMEOUT
            )
            if rating and rating.get("parentType") == 'recipe':
                await asyncio.wait_for(self.collection.update_one(query, {"$set": {"rating": update.rating}}),
                                       timeout=OPERATION_TIMEOUT)

        except asyncio.TimeoutError:
            self.logger.error(OPERATION_TIMEOUT_MESSAGE)
            raise DatabaseError()
        except Exception as e:
            self.logger.error(e)
            raise InternalError()

        if rating is None:
            self.logger.warning(f"Rating '{rating_id}' not found!")
            raise DatabaseNotFoundDataError()

    async def add_rating(self, parent_id: str, rating: Rating):
        try:
            doc = {"parentId": parent_id, **rating.dict()}
            await asyncio.wait_for(self.collection.insert_one(doc), timeout=OPERATION_TIMEOUT)

        except asyncio.TimeoutError:
            self.logger.error(OPERATION_TIMEOUT_MESSAGE)
            raise DatabaseError()
        except Exception as e:
            self.logger.error(e)
            raise InternalError()

    async def delete_rating(self, rating_id: str):
        try:
            query = {"id": rating_id}
            update_query = {
                "$set": {
                    "description": DELETED_FIELD,
                    "authorId": DELETED_FIELD
                }
            }
            rating = await asyncio.wait_for(self.collection.find_one_and_update(query, update_query),
                                            timeout=OPERATION_TIMEOUT)
            if rating and (not rating.get("children") or len(rating.get("children")) == 0):
                await asyncio.wait_for(self.collection.delete_one(query), timeout=OPERATION_TIMEOUT)

        except asyncio.TimeoutError:
            self.logger.error(OPERATION_TIMEOUT_MESSAGE)
            raise DatabaseError()
        except Exception as e:
            self.logger.error(e)
            raise InternalError()

        if rating is None:
            self.logger.warning(f"Rating '{rating_id}' not found!")
            raise DatabaseNotFoundDataError()
