from pprint import pprint

import pymongo
from pymongo import MongoClient, IndexModel, errors

print("Connecting to mongodb...", end="")
client = MongoClient("mongodb://localhost:27017/?directConnection=true")
db = client["cooking_app"]
print("Done")


def trigger_runner():
    user_collection = db["user"]
    while True:
        try:
            with user_collection.watch(
                    [{"$match": {"operationType": {"$in": ["insert", "update"]}}}],
                    full_document="updateLookup"
            ) as stream:
                for change in stream:
                    pprint(change)
        except pymongo.errors.PyMongoError as e:
            pprint(e)


if __name__ == '__main__':
    trigger_runner()
