import pymongo
from fastapi import status
from pymongo import MongoClient

from constants import *
from exceptions import IdGeneratorException


# I almost died when integrating this class
class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(MONGO_URI)
        self.counters_collection = self._connection.get_database(DB_NAME).counters

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
                    raise IdGeneratorException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCode.DB_ERROR_ID_GENERATOR)
        except IdGeneratorException as e:
            raise e
        except Exception:
            raise IdGeneratorException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCode.DB_ERROR_ACCESS)
