from api import *
from repository import RecipeCollection, UserCollection

async def delete_recipe_service(recipe_id: str):
   
    recipe_collection = RecipeCollection()
    user_collection = UserCollection()

    details = recipe_collection.get_recipe_details(recipe_id)
    ratings = details["ratings"]
    tags = details["tags"]
    allergens = details["allergens"]
    thumbnail = details["thumbnail"]
    user_id = details["authorId"]

    res = await delete_tags(tags)
    if res != 200:
        print("Tags are not deleted correctly" + res.status_code)
    
    res = await delete_allergens(allergens)
    if res != 200:
        print("Allergens are not deleted correctly" + res.status_code)
    
    res = await delete_image(thumbnail)
    if res != 200:
        print("Thumbnail is not deleted correctly" + res.status_code)

    for rating in ratings:
        res = await delete_ratings(rating)
        if res != 200:
         print("Ratings are not deleted correctly" + res.status_code)

    recipe_collection.delete_recipe(recipe_id)
    user_collection.delete_recipe_from_users(recipe_id, user_id)

    