from api import *
from repository import *
from schemas import RatingCreate
from utils import get_modify_rating_dict

client = MongoCollection()
recipe_collection = RecipeCollection(client.get_connection())
rating_collection = RatingCollection(client.get_connection())
user_collection = UserCollection(client.get_connection())


async def get_ratings(
        parent_type: str, parent_id: str, start: int, count: int, filter_query: str, sort_query: str
) -> RatingList:
    parent_type = parent_type.removesuffix("s")
    filter_query = filter_query.removesuffix("s")
    if parent_type not in [RECIPE, RATING]:
        raise RecipeRatingManagerException(
            error_code=ErrorCodes.INVALID_PARENT_TYPE, status_code=status.HTTP_404_NOT_FOUND
        )

    filter_aggregate = FILTER_DICT.get(filter_query, {})
    sort_aggregate = SORT_DICT.get(sort_query, DEFAULT_SORT)

    total, data = rating_collection.find_ratings(parent_id, start, count, filter_aggregate, sort_aggregate)
    user_cards = await fetch_user_list(list(set([rating["authorId"] for rating in data])))

    for rating in data:
        for user in user_cards.cards:
            if rating.get("authorId") == user.id:
                rating["author"] = user
                rating.pop("authorId")

    if len(data) > 0 and data[0] is not None and data[0]["parentType"] != parent_type:
        raise RecipeRatingManagerException(
            error_code=ErrorCodes.WRONG_PARENT_TYPE, status_code=status.HTTP_400_BAD_REQUEST
        )

    return RatingList(total=total, data=data)


def validate_parent(parent_id: str, parent_type: str) -> dict:
    if parent_type == RECIPE:
        parent = recipe_collection.find_recipe(parent_id)
        possible_error_code = ErrorCodes.RECIPE_NOT_FOUND
    elif parent_type == RATING:
        parent = rating_collection.find_rating_by_id(parent_id)
        possible_error_code = ErrorCodes.RATING_NOT_FOUND
    else:
        raise RecipeRatingManagerException(
            error_code=ErrorCodes.INVALID_PARENT_TYPE, status_code=status.HTTP_404_NOT_FOUND
        )

    if parent is None:
        raise RecipeRatingManagerException(
            error_code=possible_error_code, status_code=status.HTTP_404_NOT_FOUND
        )

    return parent


def add_reply(x_user_id: str, generated_id: str, body: RatingCreate, session: ClientSession):
    body.rating = 0
    rating_collection.create_rating(x_user_id, generated_id, body, session)
    update = rating_collection.update_rating(body.parentId, {"$push": {"children": generated_id}})

    if update.modified_count != 1:  # $push failed
        raise RecipeRatingManagerException(
            error_code=ErrorCodes.FAILED_ADDING_CHILD_TO_PARENT,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def add_top_level_comment(x_user_id: str, generated_id: str, recipe: dict, body: RatingCreate, session: ClientSession):
    if recipe["authorId"] == x_user_id:
        raise RecipeRatingManagerException(
            error_code=ErrorCodes.RECIPE_AUTHOR_ADDS_SELF_RATING,
            status_code=status.HTTP_403_FORBIDDEN
        )

    recipe_mods = {"$push": {"ratings": generated_id}}

    rating_collection.create_rating(x_user_id, generated_id, body, session)

    if body.rating > 0:
        recipe_mods |= get_modify_rating_dict(RatingInc.ADD_RATING, body.rating)

    recipe_collection.modify_recipe(body.parentId, recipe_mods, session)


async def post(x_user_id: str, body: RatingCreate):
    parent = validate_parent(body.parentId, body.parentType)
    generated_id = await generate_id()
    with client.get_connection().start_session() as session:
        with session.start_transaction():
            if body.parentType == RECIPE:
                add_top_level_comment(x_user_id, generated_id, parent, body, session)
            else:
                add_reply(x_user_id, generated_id, body, session)

            user_collection.update_user(x_user_id, {"$addToSet": {"ratings": generated_id}}, session)


async def modify(x_user_id: str, rating_id: str, body: RatingUpdate):
    rating = rating_collection.find_rating_by_id(rating_id)

    if rating["authorId"] != x_user_id:
        raise RecipeRatingManagerException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCodes.UNAUTHORIZED)

    if rating["parentType"] == RATING:
        body.rating = 0

    diff = body.rating - rating[RATING]
    inc: RatingInc = RatingInc.ADJUST_RATING
    if body.rating == 0 and rating[RATING] > 0:
        inc = RatingInc.REMOVE_RATING
    elif body.rating > 0 and rating[RATING] == 0:
        inc = RatingInc.ADD_RATING

    with client.get_connection().start_session() as session:
        with session.start_transaction():
            rating_collection.update_rating(
                rating_id,
                {"$set": {"description": body.description, RATING: body.rating}},
                session
            )
            if rating["parentType"] == RECIPE:
                recipe_collection.modify_recipe(rating["parentId"], get_modify_rating_dict(inc, diff), session)


def delete_top_level_comment(rating: dict, session: ClientSession):
    if rating["authorId"] == DELETED_FIELD:  # rating was previously deleted, now being pruned by child deletion
        if rating["childrenCount"] == 0:
            rating_collection.delete_rating(rating["id"], session)
            recipe_collection.modify_recipe(rating["parentId"], {"$pull": {"ratings": rating["id"]}}, session)

        return  # None

    recipe_mod = {}
    if rating["rating"] > 0:
        recipe_mod |= get_modify_rating_dict(RatingInc.REMOVE_RATING, -rating["rating"])

    if rating["authorId"] is not None and rating["authorId"] != DELETED_FIELD:
        user_collection.update_user(rating["authorId"], {"$pull": {"ratings": rating["id"]}}, session)

    if rating["childrenCount"] == 0:
        rating_collection.delete_rating(rating["id"], session)
        recipe_mod |= {"$pull": {"ratings": rating["id"]}}
        recipe_collection.modify_recipe(
            rating["parentId"],
            recipe_mod,
            session
        )
    else:
        rating_collection.update_rating(rating["id"], UPDATE_FIELDS_TO_DELETE)
        recipe_collection.modify_recipe(
            rating["parentId"],
            recipe_mod,
            session
        )


def __delete_rating_and_get_parent(rating: dict, session: ClientSession):
    rating_collection.delete_rating(rating["id"], session)
    if rating["authorId"] is not None and rating["authorId"] != DELETED_FIELD:
        user_collection.update_user(rating["authorId"], {"$pull": {"ratings": rating["id"]}}, session)
    return rating_collection.find_and_update_rating(
        rating["parentId"],
        {"$pull": {"children": rating["id"]}},
        session
    )


def delete_upwards(rating: dict, session: ClientSession):
    if rating["childrenCount"] == 0:

        parent_rating = __delete_rating_and_get_parent(rating, session)

        while parent_rating["authorId"] == DELETED_FIELD:

            parent_rating["authorId"] = None

            if parent_rating["parentType"] == RECIPE:
                return delete_top_level_comment(parent_rating, session)

            if parent_rating["childrenCount"] == 0:
                parent_rating = __delete_rating_and_get_parent(rating, session)

    else:
        rating_collection.update_rating(
            rating["id"], UPDATE_FIELDS_TO_DELETE
        )
        user_collection.update_user(rating["authorId"], {"$pull": {"ratings": rating["id"]}}, session)


def delete(x_user_id: str, rating_id: str):
    rating = rating_collection.find_rating_by_id(rating_id)
    if rating is None:
        raise RecipeRatingManagerException(
            status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCodes.RATING_NOT_FOUND
        )

    if rating["authorId"] != x_user_id:
        raise RecipeRatingManagerException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCodes.UNAUTHORIZED)

    with client.get_connection().start_session() as session:
        with session.start_transaction():
            if rating["parentType"] == RECIPE:
                delete_top_level_comment(rating, session)
            else:
                delete_upwards(rating, session)


def delete_all(x_user_id, recipe_id):
    if x_user_id != recipe_collection.find_recipe(recipe_id)["authorId"]:
        raise RecipeRatingManagerException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCodes.UNAUTHORIZED)

    with client.get_connection().start_session() as session:
        with session.start_transaction():
            data = rating_collection.get_children({"parentId": recipe_id})
            while data and len(data) > 0:
                authors, ratings = (list(t) for t in zip(*data))
                rating_collection.delete_many(ratings, session)
                user_collection.remove_ratings_from_many(authors, ratings)
                data = rating_collection.get_children({"parentId": {"$in": ratings}})

            recipe_collection.modify_recipe(recipe_id, {"$set": {"ratings": []}}, session)


async def get_rating(rating_id: str) -> RatingDataCard:
    rating = rating_collection.find_rating_by_id(rating_id)
    rating["author"] = await get_user_card(rating["authorId"])
    rating.pop("authorId")
    return RatingDataCard.model_validate(rating)


async def get_rating_by_author_and_recipe_id(recipe_id: str, author_id: str) -> RatingDataCard:
    rating = rating_collection.find_rating_by_recipe_and_author_id(recipe_id, author_id)
    rating["author"] = await get_user_card(rating["authorId"])
    rating.pop("authorId")
    return RatingDataCard.model_validate(rating)
