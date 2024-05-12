from pymongo import MongoClient
from pymongo.errors import OperationFailure, ExecutionTimeout, PyMongoError

from constants import ErrorCode, ID_PROJECTION
from exceptions import CustomException
import os

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

max_timeout_seconds = ErrorCode.MAX_TIMEOUT_TIME_SECONDS.value
max_time_ms = max_timeout_seconds * 1000


def get_next_id() -> str:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DATABASE_NAME]
        counters_collection = db.get_collection("counters")

        with client.start_session() as session:
            with session.start_transaction():
                result = counters_collection.find_one_and_update(
                    {"name": "id"},
                    {"$inc": {"value": 1}},
                    projection=ID_PROJECTION,
                    return_document=True,
                    session=session,
                    maxTimeMS=max_time_ms
                )

                if result:
                    return str(result["value"])
                else:
                    raise CustomException(status_code=500, detail=ErrorCode.ERROR_20301,
                                          headers={ErrorCode.DB_ERROR_ID_GENERATOR: ErrorCode.DB_ERROR_ID_GENERATOR})

    except (OperationFailure, ExecutionTimeout) as exc:
        raise CustomException(status_code=500, detail=str(exc), headers={ErrorCode.DB_ERROR_ID_GENERATOR: str(exc)})
    except PyMongoError as exc:
        raise CustomException(status_code=500, detail=str(exc), headers={ErrorCode.DB_ERROR_ID_GENERATOR: str(exc)})
