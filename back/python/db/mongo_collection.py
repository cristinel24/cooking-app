import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class MongoCollection:
    def __init__(self):
        self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))

    def __init__(self, connection: MongoClient):
        self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))

    def ping_db(self) -> bool:
        try:
            item = self._admin_database.command("ping")
        except Exception as e:
            raise Exception(f"Failed to ping MongoDB! - {str(e)}")
        return item

