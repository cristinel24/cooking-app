from fastapi import HTTPException
from constants import ErrorCode
from repository import MongoCollection

mongo_collection = None

def get_mongo_collection():
    global mongo_collection
    if mongo_collection is None:
        mongo_collection = MongoCollection()
    return mongo_collection

def get_next_id_services() -> str:
    try:
        collection = get_mongo_collection()
        return collection.get_next_id()
    except Exception as e:
        error_code = str(ErrorCode.DB_ERROR_ID_GENERATOR.value)
        raise HTTPException(status_code=500, detail=str(e), headers={error_code: str(e)})
