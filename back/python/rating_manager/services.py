from datetime import timezone

from api import ExternalDataProvider
from exceptions import *
from repository import RatingRepository
from schemas import *
from utils import init_logger


class RatingService:
    def __init__(self):
        self.repository = RatingRepository()
        self.provider = ExternalDataProvider()
        self.logger = init_logger("[SERVICE]")

    async def get_ratings(self, parent_id: str, start: int, count: int) -> RatingList:
        rating_list, total = await self.repository.get_ratings_of_parent(parent_id, start, count)

        async def fetch_user_rating(rating):
            user_id = rating.get("authorId", None)
            try:
                user = await self.provider.get_user(user_id)

                if isinstance(user, AuthorCardData):
                    return RatingDataCard(
                        parentId=parent_id,
                        parentType=rating["parentType"],
                        author=user,
                        updatedAt=rating["updatedAt"],
                        createdAt=rating["createdAt"],
                        rating=int(rating["rating"]),
                        description=str(rating["description"]),
                        childrenCount=len(rating["children"])
                    )

                return None

            except (ExternalError, InternalError) as e:
                self.logger.error(f"Error fetching user {user_id}. Error: {e}")

        ratings = [await fetch_user_rating(rating) for rating in rating_list]
        return RatingList(ratings=[r for r in ratings if r is not None], total=total)

    async def create_rating(self, parent_id: str, rating_data: RatingCreate):
        rating_id = await self.provider.generate_id()
        if isinstance(rating_id, str) is False:
            raise ExternalError()

        rating = Rating(
            updatedAt=datetime.now(timezone.utc),
            createdAt=datetime.now(timezone.utc),
            id=rating_id,
            authorId=rating_data.author_id,
            description=rating_data.description,
            rating=rating_data.rating,
            children=[],
            parentId=parent_id,
            parentType=rating_data.parentType
        )

        await self.repository.add_rating(parent_id, rating)
        return await card_from_rating(rating)

    async def update_rating(self, rating_id: str, rating_data: RatingUpdate):
        rating = Rating(**(await self.repository.update_rating(rating_id, rating_data)))
        return await card_from_rating(rating)

    async def delete_rating(self, rating_id: str):
        await self.repository.delete_rating(rating_id)
