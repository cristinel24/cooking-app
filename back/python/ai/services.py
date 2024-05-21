from dotenv import load_dotenv

import api
import schemas
from repository import DBWrapper
from schemas import ReplaceIngredientData
from utils.openai_client import openai_client
from utils.process_chatbot import process_chatbot_query, get_tags_from_saved_recipes
from utils.tokenize_query import tokenize_user_query, verify_generated_tokens, normalise_dict

load_dotenv()

db_wrapper = DBWrapper()
client = openai_client()


async def replace_ingredient(ingredient_schema: ReplaceIngredientData) -> dict[str, str]:
    return vars(ingredient_schema)


async def process_recipe(recipe: schemas.RecipeData) -> list[str]:

    string_to_tokenize = f"""
    titlu: {recipe.title}
    descriere: {recipe.description}
    ingrediente: {recipe.ingredients}
    pasi de preparare: {recipe.steps}
    """

    generated_tokens = await verify_generated_tokens(await tokenize_user_query(string_to_tokenize))

    # can be changed
    if recipe.prepTime < 30:
        generated_tokens["tags"].insert(0, "timp de preparare scurt")
    elif recipe.prepTime < 120:
        generated_tokens["tags"].insert(0, "timp de preparare mediu")
    else:
        generated_tokens["tags"].insert(0, "timp de preparare lung")

    position_to_insert = 1
    for tag in recipe.tags:
        generated_tokens["tags"].insert(position_to_insert, tag.lower())
        position_to_insert += 1
    for allergen in recipe.allergens:
        generated_tokens["tags"].insert(position_to_insert, allergen.lower())
        position_to_insert += 1

    return normalise_dict(generated_tokens)


async def process_query(query) -> list[str]:
    return normalise_dict(await verify_generated_tokens(await tokenize_user_query(query)))


async def process_chatbot(chatbot_input: schemas.ChatbotInput):
    user_info = db_wrapper.get_user_context(chatbot_input.userId)
    message_history = await api.get_message_history(chatbot_input.userId)
    print(message_history)
    # saved_recipe_tags = get_tags_from_saved_recipes(user_info["savedRecipes"])
    #
    # return await process_chatbot_query(
    #         user_info["messageHistory"],
    #         chatbot_input.userQuery,
    #         saved_recipe_tags,
    #         user_info["allergens"],
    #         []
    #     )
