import datetime

import httpx
from fastapi import status

import api
from constants import ErrorCodes, UNSAFE_RECIPE_DATA_FIELDS
from exception import RecipeCreatorException
from repository import MongoCollection, UserCollection, RecipeCollection
from schemas import RecipeData, Recipe
from utils import validate_recipe_data, check_flags, sanitize_html, Actions


client = MongoCollection()
user_collection = UserCollection(client.get_connection())
recipe_collection = RecipeCollection(client.get_connection())


async def create_recipe(user_id: str, recipe_data: RecipeCreationData):
    recipe_data_dict = recipe_data.model_dump()
    sanitized_fields = sanitize_html(recipe_data.model_dump(include=UNSAFE_RECIPE_DATA_FIELDS))
    for key, value in sanitized_fields.items():
        recipe_data_dict[key] = value
    validate_recipe_data(recipe_data_dict)
    recipe = Recipe(recipe_data_dict)
    try:
        recipe.id = await api.get_id()
    except httpx.ConnectError:
        raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
    recipe.tokens = await api.tokenize_recipe(recipe_data.model_dump(exclude=set("thumbnail")))
    recipe.authorId = user_id
    recipe.updatedAt = datetime.datetime.now(datetime.UTC)
    flags = 0
    try:
        with client.get_connection().start_session() as session:
            with session.start_transaction():
                user_collection.update_user(user_id, recipe.id, session)
                recipe_collection.insert_recipe(vars(recipe), session)
                await api.post_allergens(recipe.allergens, Actions.INCREMENT)
                flags += 1
                await api.post_tags(recipe.tags, Actions.INCREMENT)
                flags += 1 << 1
    except RecipeCreatorException as e:
        if check_flags(flags, 0):
            await api.post_allergens(recipe.allergens, Actions.DECREMENT)
        if check_flags(flags, 1):
            await api.post_tags(recipe.tags, Actions.DECREMENT)
        raise e
