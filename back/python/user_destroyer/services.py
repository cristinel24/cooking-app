from constants import DELETED_USER_ID
from repository import *

follow_collection = FollowCollection()
user_collection = UserCollection()
recipe_collection = RecipeCollection()
rating_collection = RatingCollection()
report_collection = ReportCollection()
expiring_token_collection = ExpiringTokenCollection()


async def delete_user(user_id: str):
    if user_collection.ping_user(user_id) is None:
        raise UserDestroyerException(ErrorCodes.NONEXISTENT_USER, 404)
    user_collection.delete_user_by_user_id(user_id)
    follow_collection.delete_follows_by_user_id(user_id)
    expiring_token_collection.delete_expiring_tokens_by_user_id(user_id)
    report_collection.update_author_id_by_user_id(user_id, DELETED_USER_ID)
    report_collection.delete_reported_id_by_user_id(user_id)
    recipe_collection.update_author_id_by_user_id(user_id, DELETED_USER_ID)
    rating_collection.update_author_id_by_user_id(user_id, DELETED_USER_ID)
