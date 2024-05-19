from api import *
from repository import RecipeCollection, UserCollection

async def delete_recipe_service(recipe_id: str):
    db = RecipeCollection()
    db_user = UserCollection()

    details = db.get_recipe_details(recipe_id)
    ratings = details["ratings"]
    tags = details["tags"]
    allergens = details["allergens"]
    user_id = details["authorId"]

    
    for rating in ratings:
        await delete_ratings(rating)
  
    for tag in tags:
        await delete_tags(tag)
    
    for allergen in allergens:
        await delete_allergens(allergen)
    
    
    db.delete_recipe(recipe_id)
    db_user.delete_recipe_from_users(recipe_id, user_id)
    
    return 0
