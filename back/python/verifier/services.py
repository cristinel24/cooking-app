from repository import UserCollection
from constants import CONFIRM_DATA_PROJECTION
from api import request_is_token_valid, request_destroy_token

user_collection = UserCollection()


async def verify(token_value: str) -> None:
    user_id = await request_is_token_valid(token_value)
    user = user_collection.get_user_by_id(user_id, CONFIRM_DATA_PROJECTION)
    user["email"] = user["login"]["newEmail"]
    user["login"]["newEmail"] = None
    user["login"]["emailStatus"] = "Confirmed"
    user_collection.update_user_by_id(user_id, user)
    await request_destroy_token(token_value)
