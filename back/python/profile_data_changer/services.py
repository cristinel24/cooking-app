from api import request_add_allergens, request_remove_allergens
from repository import UserCollection, MongoCollection
from schemas import UserProfileData, UserData
from utils import validate_user_profile_data

client = MongoCollection()
user_collection = UserCollection(client.connection)


async def patch_user(user_id: str, data: UserProfileData) -> None:
    changes = UserData(data)
    changes_dict = {key: value for key, value in vars(changes).items() if value is not None}
    validate_user_profile_data(changes_dict)
    allergens_to_add = changes_dict.pop("allergens_to_add")
    allergens_to_remove = changes_dict.pop("allergens_to_remove")
    with client.connection.start_session() as session:
        with session.start_transaction():
            user_collection.patch_user(user_id, changes_dict, allergens_to_add, allergens_to_remove, session)
            await request_add_allergens(allergens_to_add) if allergens_to_add else None
            await request_remove_allergens(allergens_to_remove) if allergens_to_remove else None
