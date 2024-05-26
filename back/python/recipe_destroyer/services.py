from api import *
from repository import RatingCollection, RecipeCollection, UserCollection
from exception import RecipeDestroyerException
recipe_collection = RecipeCollection()
user_collection = UserCollection()
rating_collection = RatingCollection()

async def delete_recipe_service(recipe_id: str, x_user_id: str):
   
    rating_arr=[]
    details = recipe_collection.get_recipe_details(recipe_id)
    ratings = details["ratings"]
    tags = details["tags"]
    allergens = details["allergens"]
    thumbnail = details["thumbnail"]
    user_id = details["authorId"]
    
    if x_user_id != user_id:
        raise RecipeDestroyerException(ErrorCodes.ACCESS_UNAUTHORIZED.value, status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        flags = 0

        await delete_tags(tags)
        flags = 1 
    
        await delete_allergens(allergens)
        flags = 2

        for rating in ratings:
            details_rating = rating_collection(rating)
            res = await delete_ratings(rating)
            if res == 200:
                rating_arr.append(details_rating)
        flags = 3   
        
        await delete_image(thumbnail)
        recipe_collection.delete_recipe(recipe_id)
        user_collection.delete_recipe_from_users(recipe_id, user_id)
    
    except RecipeDestroyerException as e:
        if flags >= 1:
            await create_tags(tags)
        if flags >= 2:
            await create_allergens(allergens)
        if flags >= 3:
            for rat in rating_arr:
                await create_ratings(recipe_id, rat)
    