from datetime import datetime
from typing import Any

from bson import ObjectId

from recipe import schemas
from db import recipe_collection
from db import rating_collection

rating_coll = rating_collection.RatingCollection()
recipe_coll = recipe_collection.RecipeCollection()

def get_recipe_ratings(data: schemas.GetRatingsData) -> list[dict]:
    try:
        recipe_id = recipe_coll.get_recipe_by_name(data.parent_name)["_id"]
        if not recipe_id:
            raise Exception("Recipe not found")
        ratings = rating_coll.get_ratings_by_recipe_id(recipe_id, data.start, data.offset)
        rating_data = []
        for rating in ratings:
            rating_data.append(
                {
                    "parent_name": data.parent_name,
                    "recipe_name": recipe_coll.get_recipe_by_id(rating["recipeId"])["name"],
                    "rating": rating["rating"],
                    "description": rating["description"],
                }
            )
        return ratings
    except Exception as e:
        raise Exception(f"Failed to get recipe ratings: {str(e)}")


def get_rating_replies(data: schemas.GetRatingsData) -> list[dict]:
    try:
        rating_id = rating_coll.get_rating_by_name(data.parent_name)["_id"]
        comments_cursor = rating_coll.get_comments_by_rating_id(rating_id, data.start, data.offset)

        def cursor_to_dict(cursor):
            result = []
            for doc in cursor:
                result.append(dict(doc))
            return result

        comments = cursor_to_dict(comments_cursor)
        print(comments)

        comment_data = []
        for comment in comments:
            comment_data.append(
                {
                    "parent_name": data.parent_name,
                    "recipe_name": recipe_coll.get_recipe_by_id(comment["recipeId"])["name"],
                    "rating": comment["rating"],
                    "description": comment["description"],
                }
            )
        return comment_data
    except Exception as e:
        raise Exception(f"Failed to get rating replies: {str(e)}")


def add_rating(data: schemas.RatingData):
    recipe_id = recipe_coll.get_recipe_by_name(data.recipe_name)["_id"]
    rating_data = {
        "name": "999",  # needs middleware to generate unique name
        "updatedAt": datetime.utcnow(),
        "authorId": ObjectId("662b8abbabbd5f853c665290"),  # need middleware to get the user id
        "recipeId": ObjectId(recipe_id),
        "rating": data.rating,
        "description": data.description,
    }
    rating_coll.insert_rating(rating_data)


def edit_rating(data: schemas.EditRatingData, parent_name: str):
    existing_rating = rating_coll.get_rating_by_name(data.rating_name)
    if existing_rating:
        recipe = recipe_coll.get_recipe_by_name(parent_name)
        if recipe and recipe["_id"] == existing_rating.get("recipeId"):
            rating_data = {
                "name": data.rating_name,
                "rating": data.rating,
                "description": data.description,
            }
            rating_coll.update_rating(existing_rating["_id"], rating_data)
        else:
            if existing_rating:
                rating_data = {
                    "name": data.rating_name,
                    "description": data.description,
                }
                rating_coll.update_rating(existing_rating["_id"], rating_data)
            else:
                return {"error": "Rating not found with the provided name/or not authorized to edit this rating"}


def delete_rating(rating_name: str):
    existing_rating = rating_coll.get_rating_by_name(rating_name)

    if existing_rating:
        rating_coll.delete_rating(existing_rating["_id"])
    else:
        return {"error": "Rating not found with the provided name"}
