import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
