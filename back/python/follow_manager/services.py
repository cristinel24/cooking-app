import httpx
from api import request_user_cards
from constants import ErrorCodes
from exception import FollowManagerException
from fastapi import status
from repository import FollowCollection, UserCollection
from schemas import *

follow_collection = FollowCollection()
user_collection = UserCollection()


async def get_followers_count(user_id: str) -> FollowersCountData:
    if user_collection.ping_user(user_id) is False:
        raise FollowManagerException(
            ErrorCodes.INVALID_USER.value, status.HTTP_404_NOT_FOUND
        )
    follower_count_data = FollowersCountData()
    follower_count_data.followers_count = follow_collection.get_followers_count(user_id)
    return follower_count_data


async def get_followers(user_id: str, start: int, count: int) -> FollowersCardsData:
    followers_cards_data = FollowersCardsData()
    request = UserCardRequestData()
    request.ids = follow_collection.get_followers(user_id, start, count)
    try:
        response = await request_user_cards(request)
    except httpx.ConnectError:
        raise FollowManagerException(
            ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE
        )
    followers_cards_data.followers = [[card for card in response.cards if card.id == id][0] for id in request.ids]
    return followers_cards_data


async def get_following_count(user_id: str) -> FollowingCountData:
    if user_collection.ping_user(user_id) is False:
        raise FollowManagerException(
            ErrorCodes.INVALID_USER.value, status.HTTP_404_NOT_FOUND
        )
    following_count_data = FollowingCountData()
    following_count_data.following_count = follow_collection.get_following_count(
        user_id
    )
    return following_count_data


async def get_following(user_id: str, start: int, count: int) -> FollowingCardsData:
    following_cards_data = FollowingCardsData()
    request = UserCardRequestData()
    request.ids = follow_collection.get_following(user_id, start, count)
    try:
        response = await request_user_cards(request)
    except httpx.ConnectError:
        raise FollowManagerException(
            ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE
        )
    following_cards_data.following = [[card for card in response.cards if card.id == id][0] for id in request.ids]
    return following_cards_data


async def add_follow(user_id: str, follows_id: str):
    if user_collection.ping_user(follows_id) is False:
        raise FollowManagerException(
            ErrorCodes.INVALID_USER.value, status.HTTP_404_NOT_FOUND
        )
    try:
        follow_collection.add_follow(user_id, follows_id)
    except FollowManagerException as e:
        if e.error_code == ErrorCodes.DB_CONNECTION_NONTIMEOUT.value:
            raise FollowManagerException(
                ErrorCodes.DUPLICATE_FOLLOW.value, status.HTTP_400_BAD_REQUEST
            )


async def delete_follow(user_id: str, follows_id: str):
    follow_collection.delete_follow(user_id, follows_id)
