from typing import Optional

from api import *
from repository import *

client = MongoCollection()

rating_collection = RatingCollection(client.get_connection())
user_collection = UserCollection(client.get_connection())
recipe_collection = RecipeCollection(client.get_connection())

def get_last_rating_value(rating_list_response: RatingListResponse) -> Optional[int]:
    if rating_list_response.ratings:
        last_rating = rating_list_response.ratings[-1]
        return last_rating.rating
    else:
        return None


async def post_recipe_services(recipe_id: str, rating_data: RatingCreateRequest, x_user_id: str):
    try:
        # Call Rating Manager to create the rating
        response = await create_rating_external(recipe_id, rating_data)
        if response.status_code != status.HTTP_200_OK:
            error = response.json()
            raise RecipeRatingManagerException(error.get("errorCode", ErrorCodes.NOT_RESPONSIVE_RATING_MANAGER.value),
                                               error.get("message", "An error occurred with the Rating Manager"))

        if rating_data.authorId != x_user_id:
            raise RecipeRatingManagerException(ErrorCodes.ACCESS_UNAUTHORIZED.value, status.HTTP_403_FORBIDDEN)
        
        # modify ratingSum and ratingCount of the User and the Recipe
        user_collection.update_user_ratings(rating_data.authorId, rating_data.rating)
        recipe_collection.update_recipe_ratings(recipe_id, rating_data.rating)

        return RatingCreateResponse(message="Rating created successfully")
    except Exception as e:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, str(e))

async def patch_recipe_services(recipe_id: str, rating_id: str, rating_data: RatingUpdateRequest,
                                x_user_id: str):
    try:
        # get previous rating value from Rating Manager
        previous_rating_response = await get_previous_ratings_external(rating_id, start=0, count=1)
        print(previous_rating_response)
        previous_rating_value = get_last_rating_value(previous_rating_response)

        # get author_id from rating, based off rating_id
        author_id = rating_collection.get_author_id_from_rating_id(rating_id)

        if author_id != x_user_id:
            raise RecipeRatingManagerException(ErrorCodes.ACCESS_UNAUTHORIZED.value, status.HTTP_403_FORBIDDEN)
        
        # adjust ratingSum and ratingCount for the recipe and user rating
        # RatingUpdateRequest has an int(rating) and a string(description)
        rating_difference = rating_data.rating - previous_rating_value

        # first parameter of the function is the author_id
        user_collection.update_user_ratings(author_id, rating_difference)
        recipe_collection.update_recipe_ratings(recipe_id, rating_difference)

        # Call Rating Manager to edit the rating
        response = await patch_rating_external(rating_id, rating_data)
        if response.status_code != status.HTTP_200_OK:
            error = response.json()
            raise RecipeRatingManagerException(error.get("errorCode", ErrorCodes.NOT_RESPONSIVE_RATING_MANAGER.value),
                                               error.get("message", "An error occurred with the Rating Manager"))

        return RatingUpdateResponse(message="Rating updated successfully")
    except Exception as e:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, str(e))

async def delete_recipe_services(recipe_id: str, rating_id: str, x_user_id: str):
    try:
        # get previous rating value from Rating Manager
        rating_list_response = await get_previous_ratings_external(rating_id, start=0, count=1)
        previous_rating_value = get_last_rating_value(rating_list_response)

        # use recipe_id to remove last recipe rating
        recipe_collection.remove_recipe_rating(recipe_id, previous_rating_value)

        # author_id = rating_collection.get_author_id_from_rating_id(rating_id)
        # identify the user
        author_id = rating_collection.get_author_id_from_rating_id(rating_id)
        if author_id != x_user_id:
            raise RecipeRatingManagerException(ErrorCodes.ACCESS_UNAUTHORIZED.value, status.HTTP_403_FORBIDDEN)

        user_collection.remove_user_rating(author_id, previous_rating_value)

        # call Rating Manager to delete the rating
        response = await delete_rating_external(RATING_MANAGER_API_URL, rating_id)
        if response.status_code != status.HTTP_200_OK:
            error = response.json()
            raise RecipeRatingManagerException(error.get("errorCode", ErrorCodes.NOT_RESPONSIVE_RATING_MANAGER.value),
                                               error.get("message", "An error occurred with the Rating Manager"))

        return RatingDeleteResponse(message="Rating deleted successfully")
    except Exception as e:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, str(e))
