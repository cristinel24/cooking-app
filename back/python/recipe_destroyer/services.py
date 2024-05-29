from api import *
from repository import RecipeCollection, UserCollection, MongoCollection

client = MongoCollection()
recipe_collection = RecipeCollection(client.get_connection())
user_collection = UserCollection(client.get_connection())


async def delete(recipe_id: str, x_user_id: str):
    try:
        recipe = await retrieve_recipe(recipe_id)
    except RecipeDestroyerException as e:
        raise e

    if recipe["author"]["id"] != x_user_id:
        raise RecipeDestroyerException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCodes.UNAUTHORIZED)

    flag: int = 0
    try:
        with client.get_connection().start_session() as session:
            with session.start_transaction():

                await delete_tags(recipe["tags"])
                flag &= 0b01

                await delete_allergens(recipe["allergens"])
                flag &= 0b10

                # cannot undo rating deletion
                try:
                    await delete_ratings(recipe["id"], x_user_id)
                except (Exception,):
                    pass

                recipe_collection.delete_recipe(recipe_id, session=session)
                user_collection.delete_recipe_from_users(recipe_id, recipe["author"]["id"], session=session)

                image_ids = extract_image_ids(recipe["description"])
                for step in recipe["steps"]:
                    image_ids.extend(extract_image_ids(step))

                # cannot undo image deletion
                for image_id in image_ids:
                    try:
                        await delete_image(image_id)
                    except (Exception,):
                        pass

    except RecipeDestroyerException as e:
        undo_steps(recipe, flag)
        raise e

    except (Exception,):
        undo_steps(recipe, flag)
        raise RecipeDestroyerException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ErrorCodes.SERVER_ERROR
        )


def extract_image_ids(rich_text: str) -> list[str]:
    return SRC_URL_FROM_IMG_TAG_REGEX.findall(rich_text)


def check_bit(flag: int, n: int) -> bool:
    return (flag & (1 << n)) == 1


def undo_steps(recipe: dict, flag: int):
    if check_bit(flag, 0):
        add_tags(recipe["tags"])
    if check_bit(flag, 1):
        add_allergens(recipe["allergens"])
