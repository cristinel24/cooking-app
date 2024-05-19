from repository import *

client = MongoCollection()
follow_collection = FollowCollection(client.get_connection())
user_collection = UserCollection(client.get_connection())
recipe_collection = RecipeCollection(client.get_connection())
rating_collection = RatingCollection(client.get_connection())
report_collection = ReportCollection(client.get_connection())
expiring_token_collection = ExpiringTokenCollection(client.get_connection())


async def delete_user(user_id: str):
    if user_collection.ping_user(user_id) is False:
        raise UserDestroyerException(ErrorCodes.NONEXISTENT_USER, 404)
    with client.get_connection().start_session() as session:
        with session.start_transaction():
            user_collection.delete_user_by_user_id(user_id, session)
            follow_collection.delete_follows_by_user_id(user_id, session)
            expiring_token_collection.delete_expiring_tokens_by_user_id(user_id, session)
            report_collection.update_author_id_by_user_id(user_id, session)
            report_collection.delete_reported_id_by_user_id(user_id, session)
            recipe_collection.update_author_id_by_user_id(user_id, session)
            rating_collection.update_author_id_by_user_id(user_id, session)
