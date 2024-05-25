from api import request_add_allergen, request_remove_allergen
from repository import UserCollection
from schemas import UserProfileData

user_collection = UserCollection()


async def patch_user(user_id: str, data: UserProfileData):
    allergens_to_add = []
    allergens_to_remove = []
    if data.allergens is not None:
        for action, allergen in data.allergens:
            match action:
                case 1:
                    allergens_to_add.append(allergen)
                case -1:
                    allergens_to_remove.append(allergen)
        data.allergens = None
    changes = {key: value for key, value in data if value is not None}
    user_collection.patch_user(user_id, changes, allergens_to_add, allergens_to_remove)
    if allergens_to_add:
        for allergen in allergens_to_add:
            await request_add_allergen(allergen)
    if allergens_to_remove:
        for allergen in allergens_to_remove:
            await request_remove_allergen(allergen)
