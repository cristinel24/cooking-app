from api import request_add_allergen, request_remove_allergen
from repository import UserCollection
from schemas import UserProfileData

user_collection = UserCollection()


async def patch_user(user_id: str, data: UserProfileData):
    changes = data.dict()
    changes.pop("allergens")
    allergens_to_add = []
    allergens_to_remove = []
    for key, value in data.allergens:
        match key:
            case 1:
                allergens_to_add.append(value)
            case -1:
                allergens_to_remove.append(value)
    user_collection.patch_user(user_id, changes)
    if allergens_to_add:
        user_collection.add_allergens(user_id, allergens_to_add)
        for allergen in allergens_to_add:
            await request_add_allergen(allergen)
    if allergens_to_remove:
        user_collection.remove_allergens(user_id, allergens_to_remove)
        for allergen in allergens_to_remove:
            await request_remove_allergen(allergen)
