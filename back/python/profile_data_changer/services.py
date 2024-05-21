from api import request_add_or_remove_allergens
from repository import UserCollection
from schemas import UserProfileData, UserData
from constants import ADD_ALLERGENS, REMOVE_ALLERGENS
from utils import sanitize_and_validate_user_profile_data

user_collection = UserCollection()


async def patch_user(user_id: str, data: UserProfileData):
    changes = UserData(data)
    changes_dict = {key: value for key, value in changes.__dict__.items() if value is not None}
    sanitize_and_validate_user_profile_data(changes_dict)
    allergens_to_add = changes_dict.pop("allergens_to_add")
    allergens_to_remove = changes_dict.pop("allergens_to_remove")
    user_collection.patch_user(user_id, changes_dict, allergens_to_add, allergens_to_remove)
    await request_add_or_remove_allergens(allergens_to_add, ADD_ALLERGENS)
    await request_add_or_remove_allergens(allergens_to_remove, REMOVE_ALLERGENS)
