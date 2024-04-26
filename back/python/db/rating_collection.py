
import pymongo.errors
from pymongo import MongoClient

from mongo_collection import MongoCollection
from bson import ObjectId


class RatingCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
<<<<<<< HEAD
        self._collection = self._connection.cooking_app.user

    
=======
        self._collection = self._connection.cooking_app.rating

>>>>>>> f552a5b16d0f0c5be3cd1816776c223cf7e5abda
    def get_rating_by_author_id(self, author_id: str):
        try:
            item = self._collection.find_one({"authorId": ObjectId(author_id)})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get rating by author id! - {str(e)}")
        return item

    def get_rating_by_name(self, rating_name: str):
        try:
            item = self._collection.find_one({"name": rating_name})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get rating column from Rating table ! - {str(e)}")
        return item

    def get_rating_by_recipe_id(self, recipe_id: str):
        try:
            item = self._collection.find_one({"recipeId": ObjectId(recipe_id)})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get rating by recipe! - {str(e)}")
        return item

    def get_rating_by_id(self, rating_id: str):
        try:
            item = self._collection.find_one({"recipeId": ObjectId(rating_id)})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get rating by recipe! - {str(e)}")
        return item

    def insert_rating(self, rating_data):
        try:
            item = self._collection.insert_one(rating_data)
            return item.inserted_id
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to insert rating! - {str(e)}")

    def update_rating(self, rating_id: str, rating_data):
        try:
            item = self._collection.update_one({"_id": ObjectId(rating_id)}, {"$set": rating_data})
            return item.modified_count
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to update rating! - {str(e)}")

    def delete_rating(self, rating_id: str):
        try:
            item = self._collection.delete_one({"_id": ObjectId(rating_id)})
            return item.deleted_count
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to delete rating! - {str(e)}")


#if __name__ == "__main__":
#coll = RatingCollection()
    #print(coll.get_rating_by_name("2msuug"))
    #print(coll.get_rating_by_recipe_id("662b8abbabbd5f853c6652c0"))
    #print(coll.get_rating_by_author_id("662b8abbabbd5f853c665297"))
    #print(coll.get_rating_by_id("662b8abbabbd5f853c6652bf"))
    #coll.delete_rating("662b8abbabbd5f853c6652bf")
    # rating_data = {
    #    "updatedAt": datetime.utcnow(),
    #       "name": "vladop",
    #      "authorId": bson.ObjectId("111111111111111111111112"),
    #     "recipeId": bson.ObjectId("111111111111111111111111"),
    #    "rating": 4,
    #   "description": "Speak other work their research more this. Wide small sometimes. Fund special by material writer special suggest audience."
    # }
    # inserted_id = coll.insert_rating(rating_data)
    # print("Inserted document ID:", inserted_id)
    #rating_data1 = {
    #   "updatedAt": datetime.utcnow(),
    #   "name": "vladox",
    #   "authorId": bson.ObjectId("111111111111111111111114"),
    #    "recipeId": bson.ObjectId("111111111111111111111113"),
    #    "rating": 4,
    #    "description": "Speak other work their research more this. Wide small sometimes. Fund special by material writer special suggest audience."
    #}
    #coll.update_rating("662bf4a1ef9351e2d0fc8ab8", rating_data1)
