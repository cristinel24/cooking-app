from logging import getLogger

from api import *
from repository import RecipeCollection, UserCollection, MongoCollection

client = MongoCollection()
recipe_collection = RecipeCollection(client.get_connection())
user_collection = UserCollection(client.get_connection())

logger = getLogger("")


async def delete_recipe_service(recipe_id: str, x_user_id: str):
    try:
        recipe = await retrieve_recipe(recipe_id)
    except RecipeDestroyerException as e:
        raise e

    if recipe["author"]["id"] != x_user_id:
        raise RecipeDestroyerException(status_code=status.HTTP_403_FORBIDDEN, error_code=ErrorCodes.UNAUTHORIZED)

    flag: int = 0
    print("create session")
    try:
        with client.get_connection().start_session() as session:
            with session.start_transaction():
                print("start transaction")
                recipe_collection.delete_recipe(recipe_id, session=session)
                user_collection.delete_recipe_from_users(recipe_id, recipe["author"]["id"], session=session)
                print("deleted")
                await delete_tags(recipe["tags"])
                flag &= 0b01
                print("deleted tags")
                await delete_allergens(recipe["allergens"])
                flag &= 0b10
                print("deleted allergens")
                # these are not redo-able
                print(recipe)
                for rating in recipe["ratings"]:
                    try:
                        await delete_rating(rating)
                    except (Exception,) as e:
                        logger.warning(e)
                print("deleted ratings")
                try:
                    await delete_image(recipe["thumbnail"])
                except (Exception,) as e:
                    logger.warning(e)

    except RecipeDestroyerException as e:
        print(f"{e.error_code} {e.status_code}")
        undo_steps(recipe, flag)
        raise e

    except (Exception,) as e:
        print(e)
        undo_steps(recipe, flag)
        raise RecipeDestroyerException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                       error_code=ErrorCodes.SERVER_ERROR)


def check_bit(flag: int, n: int) -> bool:
    return (flag & (1 << n)) == 1


def undo_steps(recipe: dict, flag: int):
    if check_bit(flag, 0):
        add_tags(recipe["tags"])
    if check_bit(flag, 1):
        add_allergens(recipe["allergens"])
