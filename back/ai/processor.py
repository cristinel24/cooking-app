from dotenv import load_dotenv
from utils.db_wrapper import DBWrapper

from utils.process_chatbot import process_chatbot_query, get_tags_from_saved_recipes
from utils.openai_client import openai_client

load_dotenv()

db_wrapper = DBWrapper()
client = openai_client()


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
