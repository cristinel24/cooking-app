import httpx

from api import request_user_cards
from constants import ErrorCodes
from exception import FollowManagerException
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
    request.ids = follow_collection.get_followers(user_id)[start:start + count]
    try:
        response = await request_user_cards(request)
    except httpx.ConnectError:
        raise FollowManagerException(ErrorCodes.NOT_RESPONSIVE_API, 503)
    user_cards = list(response.cards)
    followers_cards_data.followers = list(
        map(lambda card: UserCardData(**card), reversed(user_cards))
    )
    return followers_cards_data


async def get_following_count(user_id: str) -> FollowingCountData:
    following_count_data = FollowingCountData()
    following_count_data.following_count = len(follow_collection.get_followers(user_id))
    return following_count_data


async def get_following(user_id: str, start: int, count: int) -> FollowingCardsData:
    following_cards_data = FollowingCardsData()
    request = UserCardRequestData()
    request.ids = follow_collection.get_following(user_id)[start:start + count]
    try:
        response = await request_user_cards(request)
    except httpx.ConnectError:
        raise FollowManagerException(ErrorCodes.NOT_RESPONSIVE_API, 503)
    user_cards = list(response.cards)
    following_cards_data.following = list(
        map(lambda card: UserCardData(**card), reversed(user_cards))
    )
    return following_cards_data


async def add_follow(user_id: str, follows_id: str):
    follow = follow_collection.get_follow(user_id, follows_id)
    if follow is None:
        follow_collection.add_follow(user_id, follows_id)
    else:
        raise FollowManagerException(ErrorCodes.DUPLICATE_FOLLOW, 400)


async def delete_follow(user_id: str, follows_id: str):
    follow = follow_collection.get_follow(user_id, follows_id)
    if follow is not None:
        follow_collection.delete_follow(user_id, follows_id)
    else:
        raise FollowManagerException(ErrorCodes.NONEXISTENT_FOLLOW, 400)
