import datetime

from fastapi import status

import api
from constants import ErrorCodes, UNSAFE_RECIPE_DATA_FIELDS, UserRoles
from exception import RecipeEditorException
from repository import MongoCollection, RecipeCollection
from schemas import RecipeData, Recipe
from utils import validate_recipe_data, check_flags, sanitize_html, Actions

client = MongoCollection()
recipe_collection = RecipeCollection(client.get_connection())


async def edit_recipe(x_user_id: str, user_roles: int, recipe_id, recipe_data: RecipeData):
    sanitized_fields = sanitize_html(recipe_data.model_dump(include=UNSAFE_RECIPE_DATA_FIELDS))
    for key, value in sanitized_fields.items():
        setattr(recipe_data, key, value)
    validate_recipe_data(recipe_data)
    recipe = Recipe(recipe_data)

    recipe.updatedAt = datetime.datetime.now(datetime.UTC)
    flags = 0

    recipe_dict = await recipe_collection.get_recipe_by_id(recipe_id)

    if recipe_dict["authorId"] != x_user_id and not user_roles & UserRoles.ADMIN:
        raise RecipeEditorException(ErrorCodes.FORBIDDEN_USER.value, status.HTTP_403_FORBIDDEN)

    try:
        with client.get_connection().start_session() as session:
            with session.start_transaction():
                # regenerate tokens
                fields_needed = ["title", "prepTime", "tags", "allergens", "description", "ingredients", "steps"]
                ans = await api.tokenize_recipe(
                    {key: (recipe_dict[key] if not hasattr(recipe, key) else getattr(recipe, key)) for key in
                     fields_needed})
                if ans is not None:
                    recipe.tokens = ans

                await recipe_collection.edit_recipe(recipe_id, vars(recipe), session)

                if recipe_data.allergens is not None:
                    allergens_to_delete = [item for item in recipe_dict["allergens"] if item not in recipe.allergens]
                    allergens_to_add = [item for item in recipe.allergens if item not in recipe_dict["allergens"]]
                    await api.post_allergens(allergens_to_delete, Actions.DECREMENT)
                    flags += 1
                    await api.post_allergens(allergens_to_add, Actions.INCREMENT)
                    flags += 1 << 1

                if recipe_data.tags is not None:
                    tags_to_delete = [item for item in recipe_dict["tags"] if item not in recipe.tags]
                    tags_to_add = [item for item in recipe.tags if item not in recipe_dict["tags"]]
                    await api.post_tags(tags_to_delete, Actions.DECREMENT)
                    flags += 1 << 2
                    await api.post_tags(tags_to_add, Actions.INCREMENT)
                    flags += 1 << 3

    except RecipeEditorException as e:
        if check_flags(flags, 0):
            await api.post_allergens(allergens_to_delete, Actions.INCREMENT)
        if check_flags(flags, 1):
            await api.post_allergens(allergens_to_add, Actions.DECREMENT)
        if check_flags(flags, 2):
            await api.post_tags(tags_to_delete, Actions.INCREMENT)
        if check_flags(flags, 3):
            await api.post_tags(tags_to_add, Actions.DECREMENT)
        raise e
