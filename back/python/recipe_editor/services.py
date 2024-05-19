import datetime

from fastapi import status
import api
from exception import RecipeEditorException
from repository import MongoCollection, RecipeCollection
from schemas import RecipeData, Recipe
from utils import validate_recipe_data, check_flags
from constants import ErrorCodes

client = MongoCollection()
recipe_collection = RecipeCollection(client.get_connection())


async def edit_recipe(x_user_id: str, recipe_id, recipe_data: RecipeData):
    validate_recipe_data(recipe_data)
    recipe = Recipe(recipe_data)

    recipe.tokens = await api.tokenize_recipe(recipe_data.model_dump(exclude=set("thumbnail")))
    recipe.updatedAt = datetime.datetime.now(datetime.UTC)
    flags = 0

    try:
        with client.get_connection().start_session() as session:
            with session.start_transaction():
                recipe_dict = recipe_collection.get_recipe_by_id(recipe_id, session)

                if recipe_dict["authorId"] != x_user_id:
                    raise RecipeEditorException(ErrorCodes.ACCESS_UNAUTHORIZED.value, status.HTTP_403_FORBIDDEN)

                recipe_collection.edit_recipe(recipe_id, vars(recipe), session)
                # await api.add_allergens(recipe.allergens)
                # flags += 1
                # await api.add_tags(recipe.tags)
                # flags += 1 << 1
    except RecipeEditorException as e:
        # if check_flags(flags, 0):
        #     await api.delete_allergens(recipe.allergens)
        # if check_flags(flags, 1):
        #     await api.delete_tags(recipe.tags)
        raise e
