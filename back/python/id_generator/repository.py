from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import OperationFailure, ExecutionTimeout, PyMongoError

from constants import ID_PROJECTION
from constants import ERROR_20301
from exceptions import CustomException
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


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
                    maxTimeMS=10000  # 10 seconds timeout
                )

                if result:
                    return str(result["value"])
                else:
                    raise CustomException(status_code=500, detail=ERROR_20301, headers={ERROR_20301: ERROR_20301})
    except (OperationFailure, ExecutionTimeout) as exc:
        raise CustomException(status_code=500, detail=str(exc), headers={ERROR_20301: str(exc)})
    except PyMongoError as exc:
        raise CustomException(status_code=500, detail=str(exc), headers={ERROR_20301: str(exc)})
