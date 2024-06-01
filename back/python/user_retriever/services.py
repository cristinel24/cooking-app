from constants import USER_DATA_PROJECTION, USER_CARD_DATA_PROJECTION, USER_FULL_DATA_PROJECTION
from repository import UserCollection
from schemas import *
from utils import calculate_avg_rating
from api import *

user_collection = UserCollection()


async def get_user_data(user_id: str, x_user_id: str | None) -> UserData:
    user_data = user_collection.get_user_by_id(user_id, USER_DATA_PROJECTION)
    avg_rating = calculate_avg_rating(user_data)
    user_data["ratingAvg"] = avg_rating
    follows_count = await request_user_following_count(user_id)
    followers_count = await request_user_followers_count(user_id)
    user_data["followsCount"] = follows_count
    user_data["followersCount"] = followers_count
    if user_id != x_user_id and x_user_id is not None:
        follow_response = await request_get_follow(user_id, x_user_id)
        user_data["isFollowedBy"] = follow_response["followed"]
        user_data["isFollowing"] = follow_response["following"]
    else:
        user_data["isFollowedBy"] = None
        user_data["isFollowing"] = None
    return UserData(**user_data)


async def get_user_card_data(user_id: str, x_user_id: str | None) -> UserCardData:
    user_data = user_collection.get_user_by_id(user_id, USER_CARD_DATA_PROJECTION)
    avg_rating = calculate_avg_rating(user_data)
    user_data["ratingAvg"] = avg_rating
    if user_id != x_user_id and x_user_id is not None:
        follow_response = await request_get_follow(user_id, x_user_id)
        user_data["isFollowedBy"] = follow_response["followed"]
        user_data["isFollowing"] = follow_response["following"]
    else:
        user_data["isFollowedBy"] = None
        user_data["isFollowing"] = None
    return UserCardData(**user_data)


async def get_user_cards_data(user_ids: list[str], x_user_id: str | None) -> list[UserCardData]:
    users_data = user_collection.get_users_by_id(user_ids, USER_CARD_DATA_PROJECTION)
    for user_data in users_data:
        avg_rating = calculate_avg_rating(user_data)
        user_data["ratingAvg"] = avg_rating
        if user_data["id"] != x_user_id and x_user_id is not None:
            follow_response = await request_get_follow(user_data["id"], x_user_id)
            user_data["isFollowedBy"] = follow_response["followed"]
            user_data["isFollowing"] = follow_response["following"]
        else:
            user_data["isFollowedBy"] = None
            user_data["isFollowing"] = None
    return [UserCardData(**user_data) for user_data in users_data]


async def get_user_full_data(user_id: str) -> UserFullData:
    user_data = user_collection.get_user_by_id(user_id, USER_FULL_DATA_PROJECTION)
    avg_rating = calculate_avg_rating(user_data)
    user_data["ratingAvg"] = avg_rating
    follows_count = await request_user_following_count(user_id)
    followers_count = await request_user_followers_count(user_id)
    user_data["followsCount"] = follows_count
    user_data["followersCount"] = followers_count
    return UserFullData(**user_data)
