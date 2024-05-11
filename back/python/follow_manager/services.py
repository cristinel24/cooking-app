from api import request_user_cards
from repository import FollowCollection
from schemas import *

follow_collection = FollowCollection()


async def get_followers_count(user_id: str) -> FollowersCountData:
    follower_count_data = FollowersCountData()
    follower_count_data.followers_count = len(follow_collection.get_followers(user_id))
    return follower_count_data


async def get_followers(user_id: str, start: int, count: int) -> FollowersCardsData:
    followers_cards_data = FollowersCardsData()
    request = UserCardRequestData()
    request.ids = follow_collection.get_followers(user_id)
    response = await request_user_cards(request)
    user_cards = list(response.cards)[start:start + count]
    followers_cards_data.followers = list(
        map(lambda card: UserCardData(**card), user_cards)
    )
    return followers_cards_data


async def get_following_count(user_id: str) -> FollowingCountData:
    following_count_data = FollowingCountData()
    following_count_data.following_count = len(follow_collection.get_followers(user_id))
    return following_count_data


async def get_following(user_id: str, start: int, count: int) -> FollowingCardsData:
    following_cards_data = FollowingCardsData()
    request = UserCardRequestData()
    request.ids = follow_collection.get_following(user_id)
    response = await request_user_cards(request)
    user_cards = list(response.cards)[start:start + count]
    following_cards_data.following = list(
        map(lambda card: UserCardData(**card), user_cards)
    )
    return following_cards_data
