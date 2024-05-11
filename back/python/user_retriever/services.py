from constants import USER_DATA_PROJECTION, USER_CARD_DATA_PROJECTION, USER_FULL_DATA_PROJECTION, ErrorCodes
from repository import UserCollection
from schemas import *
from utils import calculate_avg_rating, pop_rating_sum_and_count
from api import *

user_collection = UserCollection()


async def get_user_data(user_id: str) -> UserData:
    try:
        user_data = user_collection.get_user_by_id(user_id, USER_DATA_PROJECTION)
        avg_rating = calculate_avg_rating(user_data)
        user_data["ratingAvg"] = avg_rating
        pop_rating_sum_and_count(user_data)
        return UserData(**user_data)
    except Exception as e:
        raise Exception(e)


async def get_user_card_data(user_id: str) -> UserCardData:
    try:
        user_data = user_collection.get_user_by_id(user_id, USER_CARD_DATA_PROJECTION)
        avg_rating = calculate_avg_rating(user_data)
        user_data["ratingAvg"] = avg_rating
        pop_rating_sum_and_count(user_data)
        return UserCardData(**user_data)
    except Exception as e:
        raise Exception(e)


async def get_user_cards_data(user_ids: list[str]) -> list[UserCardData]:
    try:
        users_data = user_collection.get_users_by_id(user_ids, USER_CARD_DATA_PROJECTION)
        for user_data in users_data:
            avg_rating = calculate_avg_rating(user_data)
            user_data["ratingAvg"] = avg_rating
            pop_rating_sum_and_count(user_data)
        return [UserCardData(**user_data) for user_data in users_data]
    except Exception as e:
        raise Exception(e)


async def get_user_full_data(user_id: str) -> UserFullData:
    try:
        user_data = user_collection.get_user_by_id(user_id, USER_FULL_DATA_PROJECTION)
        avg_rating = calculate_avg_rating(user_data)
        user_data["ratingAvg"] = avg_rating
        pop_rating_sum_and_count(user_data)
        follows_count = await request_user_following_count(user_id)
        followers_count = await request_user_followers_count(user_id)
        user_data["followsCount"] = follows_count
        user_data["followersCount"] = followers_count
        return UserFullData(**user_data)
    except Exception as e:
        raise Exception(e)
