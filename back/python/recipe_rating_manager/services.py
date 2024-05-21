from fastapi import status
from exceptions import RecipeRatingManagerException
from api import *
from repository import *

client = MongoCollection

user_collection = UserCollection(client.get_connection())
recipe_collection = RecipeCollection(client.get_connection())

async def put_recipe(recipe_id: str, rating_data: RatingCreateRequest):
    try:
        # Call Rating Manager to create the rating
        response = await update_recipe_rating(recipe_id, rating_data.authorId, rating_data)

        # Modify ratingSum and ratingCount of the User and the Recipe
        user_collection.update_user_ratings(rating_data.authorId, rating_data.rating)
        recipe_collection.update_recipe_ratings(recipe_id, rating_data.rating)

        return RatingCreateResponse(message="Rating created successfully")
    except Exception as e:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, str(e))

async def patch_recipe(recipe_id: str, rating_id: str, rating_data: RatingUpdateRequest):
    try:
        # Get previous rating value from Rating Manager
        previous_rating_response = await get_ratings(rating_id, start=0, count=1, user_id="")
        previous_rating_value = previous_rating_response.ratings[0].rating

        # Adjust ratingSum and ratingCount for the recipe and user rating
        rating_difference = rating_data.rating - previous_rating_value
        user_collection.update_user_ratings(rating_id, rating_difference)
        recipe_collection.update_recipe_ratings(recipe_id, rating_difference)

        # Call Rating Manager to edit the rating
        response = await update_rating(rating_id, rating_data.authorId, rating_data)

        return RatingUpdateResponse(message="Rating updated successfully")
    except Exception as e:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, str(e))

async def delete_recipe(recipe_id: str, rating_id: str):
    try:
        # Get previous rating value from Rating Manager
        previous_rating_response = await get_ratings(rating_id, start=0, count=1, user_id="")
        previous_rating_value = previous_rating_response.ratings[0].rating

        # Remove rating value from the recipe and user rating
        user_collection.remove_user_rating(rating_id, previous_rating_value)
        recipe_collection.remove_recipe_rating(recipe_id, previous_rating_value)

        # Call Rating Manager to delete the rating
        await delete_rating(RATING_MANAGER_API_URL, rating_id)

        return RatingDeleteResponse(message="Rating deleted successfully")
    except Exception as e:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, str(e))
