from repository import UserCollection
from api import request_is_token_valid, request_destroy_token
from constants import PIPELINE_EMAIL_CHANGE

user_collection = UserCollection()


async def verify(token_value: str) -> None:
    user_id = await request_is_token_valid(token_value)
    await request_destroy_token(token_value)
    user_collection.update_user_by_id(user_id, PIPELINE_EMAIL_CHANGE)
