from api import *
from repository import RatingCollection, RecipeCollection, UserCollection

async def delete_recipe_service(recipe_id: str):
   
    recipe_collection = RecipeCollection()
    user_collection = UserCollection()
    rating_collection = RatingCollection()

    rating_arr=[]
    details = recipe_collection.get_recipe_details(recipe_id)
    ratings = details["ratings"]
    tags = details["tags"]
    allergens = details["allergens"]
    thumbnail = details["thumbnail"]
    user_id = details["authorId"]

    
    res = await delete_tags(tags)
    if res != 200:
        return 
    
    res = await delete_allergens(allergens)
    if res != 200:
        await create_tags(tags)
        return 
    
    for rating in ratings:
        details_rating = rating_collection(rating)
        res = await delete_ratings(rating)
        if res == 200:
            rating_arr.append(details_rating)
        else:
            await create_tags(tags)
            await create_allergens(allergens)
            for rat in rating_arr:
                await create_ratings(recipe_id, rat)
            return 
        
    res = await delete_image(thumbnail)
    if res != 200:
        res = await create_tags(tags)
        await create_allergens(allergens)
        for rat in rating_arr:
            await create_ratings(recipe_id, rat)
        return
     
    recipe_collection.delete_recipe(recipe_id)
    user_collection.delete_recipe_from_users(recipe_id, user_id)

    

    