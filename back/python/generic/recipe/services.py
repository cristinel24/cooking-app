from datetime import datetime
from bson import ObjectId

from generic.recipe import schemas
from db import recipe_collection, rating_collection, user_collection

rating_coll = rating_collection.RatingCollection()
recipe_coll = recipe_collection.RecipeCollection()
user_coll = user_collection.UserCollection()


def get_recipe(recipe_name: str) -> dict:
    return recipe_coll.get_recipe_by_name(recipe_name)


def get_recipe_card(recipe_name: str) -> dict:
    recipe_card = recipe_coll.get_recipe_by_name(recipe_name)
    recipe_card.pop("_id")
    # recipe_card["author"] = user_coll.get_user_by_id(recipe_card["authorId"])
    recipe_card.pop("authorId")
    recipe_card.pop("ratings")
    return recipe_card


def add_tokens(recipe_name: str, recipe_tokens: list[str]) -> None:
    recipe_coll.add_tokens_by_name(recipe_name, recipe_tokens)


def create_recipe(data) -> None:
    recipe_coll.insert_recipe(data)


def update_recipe(data: dict) -> None:
    recipe_coll.update_recipe_by_name(data)


def delete_recipe(name: str):
    return recipe_coll.delete_recipe_by_name(name)


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
                    "recipe_name": data.parent_name,
                    "rating": rating["rating"],
                    "description": rating["description"],
                }
            )
        return rating_data
    except Exception as e:
        raise Exception(f"Failed to get recipe ratings: {str(e)}")


def get_rating_replies(data: schemas.GetRatingsData) -> list[dict]:
    try:
        rating_id = rating_coll.get_rating_by_name(data.parent_name)["_id"]
        comments = rating_coll.get_comments_by_rating_id(rating_id, data.start, data.offset)

        comment_data = []
        for comment in comments:
            comment_data.append(
                {
                    "parent_name": data.parent_name,
                    "rating": comment["rating"],
                    "description": comment["description"],
                }
            )
        return comment_data
    except Exception as e:
        raise Exception(f"Failed to get rating replies: {str(e)}")


def add_rating(data: schemas.RatingData):
    # TODO: add extra validation for data
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
