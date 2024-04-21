from dotenv import load_dotenv
from utils.db_wrapper import DBWrapper
from utils.tokenize_query import tokenize_user_query, verify_generated_tokens, normalise_dict

from utils.process_chatbot import process_chatbot_query, get_tags_from_saved_recipes
from utils.openai_client import openai_client

load_dotenv()

db_wrapper = DBWrapper()
client = openai_client()


async def process_recipe(recipe):
    recipe_dict = dict(recipe)
    print(recipe_dict)

    string_to_tokenize = f"""titlu: {recipe_dict["title"]}
    descriere: {recipe_dict["description"]}
    ingrediente: {recipe_dict["ingredients"]}
    pasi de preparare: {recipe_dict["prepare_steps"]}
    """
    print(string_to_tokenize)

    generated_tokens = await verify_generated_tokens(await tokenize_user_query(string_to_tokenize))

    # can be changed
    if int(recipe_dict["prepare_time"]) < 30:
        generated_tokens["tags"].insert(0, "timp de preparare scurt")
    elif int(recipe_dict["prepare_time"]) > 120:
        generated_tokens["tags"].insert(0, "timp de preparare lung")
    else:
        generated_tokens["tags"].insert(0, "timp de preparare mediu")

    position_to_insert = 1
    for tag in recipe_dict["tags"]:
        generated_tokens["tags"].insert(position_to_insert, tag.lower())
        position_to_insert += 1
    for allergen in recipe_dict["allergens"]:
        generated_tokens["tags"].insert(position_to_insert, allergen.lower())
        position_to_insert += 1

    return normalise_dict(generated_tokens)


async def process_query(query):
    return normalise_dict(await verify_generated_tokens(await tokenize_user_query(query)))


async def process_chatbot(api_query):
    query = dict(api_query)
    user_id = query["user_id"]
    user_query = query["user_query"]

    user_info = db_wrapper.get_user_context(user_id)

    saved_recipe_tags = get_tags_from_saved_recipes(user_info["savedRecipes"])

    return {
        "message": await process_chatbot_query(
            user_info["messageHistory"],
            user_query,
            user_info["tags"],
            saved_recipe_tags,
            user_info["allergens"],
            []
        )
    }
