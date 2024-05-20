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

    recipe.updatedAt = datetime.datetime.now(datetime.UTC)
    flags = 0

    try:
        with client.get_connection().start_session() as session:
            with session.start_transaction():
                recipe_dict = await recipe_collection.get_recipe_by_id(recipe_id, session)
                if recipe_dict["authorId"] != x_user_id:
                    raise RecipeEditorException(ErrorCodes.ACCESS_UNAUTHORIZED.value, status.HTTP_403_FORBIDDEN)

                await recipe_collection.edit_recipe(recipe_id, vars(recipe), session)

                if recipe_data.allergens is not None:
                    allergens_to_delete = [item for item in recipe_dict["allergens"] if item not in recipe.allergens]
                    allergens_to_add = [item for item in recipe.allergens if item not in recipe_dict["allergens"]]
                    await api.delete_allergens(allergens_to_delete)
                    flags += 1
                    await api.add_allergens(allergens_to_add)
                    flags += 1 << 1

                if recipe_data.tags is not None:
                    tags_to_delete = [item for item in recipe_dict["tags"] if item not in recipe.tags]
                    tags_to_add = [item for item in recipe.tags if item not in recipe_dict["tags"]]
                    await api.delete_tags(tags_to_delete)
                    flags += 1 << 2
                    await api.add_tags(tags_to_add)
                    flags += 1 << 3

                # regenerate tokens and edit them
                new_recipe_dict = await recipe_collection.get_recipe_by_id(recipe_id, session)
                fields_needed = ["title", "prepTime", "tags", "allergens", "description", "ingredients", "steps"]
                recipe.tokens = await api.tokenize_recipe({key: new_recipe_dict[key] for key in fields_needed})
                await recipe_collection.edit_recipe(recipe_id, {"tokens": recipe.tokens}, session)
                flags += 1 << 4

    except RecipeEditorException as e:
        with client.get_connection().start_session() as session:
            with session.start_transaction():
                await recipe_collection.edit_recipe(recipe_id, recipe_dict, session)
                if check_flags(flags, 0):
                    await api.add_allergens(allergens_to_delete)
                if check_flags(flags, 1):
                    await api.delete_allergens(allergens_to_add)
                if check_flags(flags, 2):
                    await api.add_tags(tags_to_delete)
                if check_flags(flags, 3):
                    await api.delete_tags(tags_to_add)
                if check_flags(flags, 4):
                    # tokens are already restored at the first glance
                    pass
                raise e
