from fastapi import HTTPException
from constants import ErrorCode
from repository import MongoCollection

def get_next_id_services() -> str:
    try:
        mongo_collection = MongoCollection()
        return mongo_collection.get_next_id()
    except Exception as e:
        error_code = str(ErrorCode.DB_ERROR_ID_GENERATOR.value)
        raise HTTPException(status_code=500, detail=str(e), headers={error_code: str(e)})
