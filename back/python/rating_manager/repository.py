import pymongo.errors
from motor.motor_asyncio import AsyncIOMotorClient

from schemas import Rating, RatingUpdate
from constants import (
    MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION, RATING_PROJECTION, DELETED_FIELD, DatabaseError, InternalError,
    DatabaseNotFoundDataError
)
from utils import singleton, init_logger

OPERATION_TIMEOUT: int = 10


@singleton
class RatingRepository:
    def __init__(self, db_url: str = MONGO_URI,
                 db_name: str = MONGO_DATABASE,
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

            with pymongo.timeout(OPERATION_TIMEOUT):
                cursor = self.collection.aggregate(pipeline, allowDiskUse=True)
            ratings = await cursor.to_list(length=count)

            total_pipeline = [{"$match": {"parentId": parent_id}}, {"$count": "total"}]
            with pymongo.timeout(OPERATION_TIMEOUT):
                total_result = await self.collection.aggregate(total_pipeline).next()
            total = total_result.get("total", 0)

            return ratings, total
        except pymongo.errors.PyMongoError as e:
            self.logger.error(e)
            raise DatabaseError()
        except Exception as e:
            self.logger.error(e)
            raise InternalError()

    async def update_rating(self, rating_id: str, update: RatingUpdate):
        try:
            query = {"id": rating_id}
            with pymongo.timeout(OPERATION_TIMEOUT):
                rating = await self.collection.find_one_and_update(query, {"$set": {"description": update.description}})
                if rating and rating.get("parentType") == 'recipe':
                    await self.collection.update_one(query, {"$set": {"rating": update.rating}})

        except pymongo.errors.PyMongoError as e:
            self.logger.error(e)
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
            with pymongo.timeout(OPERATION_TIMEOUT):
                await self.collection.insert_one(doc)

        except pymongo.errors.PyMongoError as e:
            self.logger.error(e)
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
            with pymongo.timeout(OPERATION_TIMEOUT):
                rating = await self.collection.find_one_and_update(query, update_query)
                if rating and (not rating.get("children") or len(rating.get("children")) == 0):
                    await self.collection.delete_one(query)

        except pymongo.errors.PyMongoError as e:
            self.logger.error(e)
            raise DatabaseError()

        except Exception as e:
            self.logger.error(e)
            raise InternalError()

        if rating is None:
            self.logger.warning(f"Rating '{rating_id}' not found!")
            raise DatabaseNotFoundDataError()
