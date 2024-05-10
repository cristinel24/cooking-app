from dotenv import load_dotenv
from fastapi import HTTPException
from pymongo import MongoClient
from constants import ERROR_20301
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

def get_next_id() -> str:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    counters_collection = db.get_collection("counters")
    result = counters_collection.find_one_and_update(
        {"name": "id"},
        {"$inc": {"value": 1}},
        return_document=True
    )
    if result:
        print(result)
        return str(result["value"])
    else:
        error_message = "Failed to fetch or update the ID"
        raise HTTPException(status_code=500, detail=error_message, headers={ERROR_20301: error_message})