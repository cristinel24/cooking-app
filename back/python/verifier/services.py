from repository import UserCollection
from api import request_is_token_valid, request_destroy_token
from constants import NEW_EMAIL_PROJECTION

user_collection = UserCollection()


async def verify(token_value: str) -> None:
    user_id = await request_is_token_valid(token_value)
    user = user_collection.get_user_by_id(user_id, NEW_EMAIL_PROJECTION)
    print(user)
    changes = {
        "email": user["login"]["newEmail"],
        "login.newEmail": None,
        "login.emailStatus": "Confirmed"
    }
    user_collection.update_user_by_id(user_id, changes)
    await request_destroy_token(token_value)
