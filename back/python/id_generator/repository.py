import os

import pymongo
from pymongo import MongoClient, errors
from constants import ErrorCode, ID_PROJECTION, MAX_TIMEOUT_TIME_SECONDS
from exceptions import CustomException

class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(os.getenv("MONGO_URI"))
        self.counters_collection = self._connection[os.getenv("DATABASE_NAME")][os.getenv("COUNTERS_COLLECTION")]

    def get_next_id(self) -> str:
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                result = self.counters_collection.find_one_and_update(
                    {"name": "id"},
                    {"$inc": {"value": 1}},
                    projection=ID_PROJECTION,
                    return_document=True,
                )
                if result:
                    return result["value"]
                else:
                    raise CustomException(status_code=500, detail=ErrorCode.DB_ERROR_ID_GENERATOR.value,
                                          headers={ErrorCode.DB_ERROR_ID_GENERATOR: ErrorCode.DB_ERROR_ID_GENERATOR})
        except pymongo.errors.ExecutionTimeout as exc:
            raise CustomException(status_code=500, detail=str(exc), headers={ErrorCode.DB_ERROR_ID_GENERATOR: str(exc)})
        except errors.PyMongoError as exc:
            raise CustomException(status_code=500, detail=str(exc), headers={ErrorCode.DB_ERROR_ID_GENERATOR: str(exc)})
