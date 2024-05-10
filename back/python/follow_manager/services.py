from repository import FollowCollection
from schemas import *

follow_collection = FollowCollection()


async def get_followers_count(user_id: str) -> FollowersCountData:
    follower_count_data = FollowersCountData()
    follower_count_data.followers_count = len(follow_collection.get_followers(user_id))
    return follower_count_data


async def get_followers(user_id: str, start: int, count: int) -> FollowersCardsData:
    pass


async def get_following_count(user_id: str) -> FollowingCountData:
    following_count_data = FollowingCountData()
    following_count_data.following_count = len(follow_collection.get_followers(user_id))
    return following_count_data
