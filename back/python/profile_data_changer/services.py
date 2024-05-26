from api import request_inc_allergens, request_dec_allergens
from constants import UNSAFE_USER_DATA_FIELDS
from repository import UserCollection, MongoCollection
from schemas import UserProfileData, UserData
from utils import validate_user_profile_data, sanitize_html

client = MongoCollection()
user_collection = UserCollection(client.connection)


async def patch_user(user_id: str, data: UserProfileData) -> None:
    sanitized_fields = sanitize_html(data.model_dump(include=UNSAFE_USER_DATA_FIELDS))
    for key, value in sanitized_fields.items():
        setattr(data, key, value)
    changes = {key: value for key, value in vars(UserData(data)).items() if value is not None}
    validate_user_profile_data(changes)
    allergens_to_add = changes.pop("allergens_to_add")
    allergens_to_remove = changes.pop("allergens_to_remove")
    with client.connection.start_session() as session:
        with session.start_transaction():
            user_collection.patch_user(user_id, changes, allergens_to_add, allergens_to_remove, session)
            await request_inc_allergens(allergens_to_add) if allergens_to_add else None
            await request_dec_allergens(allergens_to_remove) if allergens_to_remove else None
