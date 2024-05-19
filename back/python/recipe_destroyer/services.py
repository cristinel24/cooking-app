from api import *
from repository import * 

async def delete_recipe_service(recipe_id: str):
    
    db = RecipeCollection()
    db_user=UserCollection()
    
    ratings = db.get_ratings_from_recipe(recipe_id)
    print(ratings)
    tags = db.get_tags_from_recipe(recipe_id)
    allergens = db.get_allergens_from_recipe(recipe_id)
    user_id = db.get_author_from_recipe(recipe_id)
    
    if isinstance(ratings,list) and ratings != []:
        for rating in ratings:
            await delete_ratings(rating)

    if isinstance(tags, list) and tags != []:
        for tag in tags:
            await delete_tags(tag)
    
    if isinstance(allergens, list) and allergens != []:
        for allergen in allergens:
            await delete_allergens(allergen)
    
    
    db.delete_recipe_mongo(recipe_id)
    db_user.delete_recipe_from_users_mongo(recipe_id, user_id)
    return 0
