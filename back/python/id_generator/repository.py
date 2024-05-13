import os

import pymongo
from pymongo import MongoClient
from pymongo.errors import OperationFailure, PyMongoError

from constants import ErrorCode, ID_PROJECTION, MAX_TIMEOUT_TIME_SECONDS
from exceptions import CustomException

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

def connect_to_database(database_name: str) -> pymongo.collection.Collection:
    try:
        db = client[database_name]
        counters_collection = db.get_collection("counters")
        return counters_collection
    except Exception as e:
        error_code = ErrorCode.DB_ERROR_ACCESS
        error_message = f"Error accessing database: {e}"
        raise CustomException(status_code=500, detail=error_message, headers={error_code: error_code})


def get_next_id() -> str:
    try:
        counters_collection = connect_to_database(DATABASE_NAME)
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = counters_collection.find_one_and_update(
                {"name": "id"},
                {"$inc": {"value": 1}},
                projection=ID_PROJECTION,
                return_document=True,
            )

            if result:
                return str(result["value"])
            else:
                raise CustomException(status_code=500, detail=ErrorCode.ERROR_20301,
                                      headers={ErrorCode.DB_ERROR_ID_GENERATOR: ErrorCode.DB_ERROR_ID_GENERATOR})

    except pymongo.errors.ExecutionTimeout as exc:
        raise CustomException(status_code=500, detail=str(exc), headers={ErrorCode.DB_ERROR_ID_GENERATOR: str(exc)})
    except PyMongoError as exc:
        raise CustomException(status_code=500, detail=str(exc), headers={ErrorCode.DB_ERROR_ID_GENERATOR: str(exc)})
