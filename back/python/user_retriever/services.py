from pprint import pprint

from constants import USER_DATA_PROJECTION, USER_CARD_DATA_PROJECTION, USER_FULL_DATA_PROJECTION
from repository import UserCollection
from schemas import UserData, UserCardData, UserFullData
from utils import calculate_avg_rating

user_collection = UserCollection()


async def get_user_data(user_id: str) -> UserData:
    user_data = user_collection.get_user_by_id(user_id, USER_DATA_PROJECTION)
    avg_rating = calculate_avg_rating(user_data)
    user_data["ratingAvg"] = avg_rating
    return UserData(**user_data)


async def get_user_card_data(user_id: str) -> UserCardData:
    user_data = user_collection.get_user_by_id(user_id, USER_CARD_DATA_PROJECTION)
    avg_rating = calculate_avg_rating(user_data)
    user_data["ratingAvg"] = avg_rating
    return UserCardData(**user_data)


async def get_user_cards_data(user_ids: list[str]) -> list[UserCardData]:
    users_data = user_collection.get_users_by_id(user_ids, USER_CARD_DATA_PROJECTION)
    for user_data in users_data:
        avg_rating = calculate_avg_rating(user_data)
        user_data["ratingAvg"] = avg_rating
    return [UserCardData(**user_data) for user_data in users_data]

# async def get_user_full_data(user_id: str) -> UserFullData:
#    user_data = user_collection.get_user_by_id(user_id, USER_FULL_DATA_PROJECTION)
#    avg_rating = calculate_avg_rating(user_data)
#    user_data["ratingAvg"] = avg_rating
#    return UserFullData(**user_data)
