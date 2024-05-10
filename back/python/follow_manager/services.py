from repository import FollowCollection
from schemas import AuthFollowData

follow_collection = FollowCollection()


async def get_follower_count(user_id: str) -> dict:
    return {
        "followersCount": len(follow_collection.get_followers(user_id))
    }


async def get_following_count(user_id: str) -> dict:
    return {
        "followingCount": len(follow_collection.get_following(user_id))
    }
