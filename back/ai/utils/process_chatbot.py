from . import constants
from .db_wrapper import DBWrapper
from .openai_client import openai_client

db_wrapper = DBWrapper()
client = openai_client()


async def process_chatbot_query(message_history: list[str], user_query: str,
                                user_tags: list[str], saved_recipe_tokens: list[str],
                                allergens: list[str], blacklisted_items: list[str]) -> str:
    header_start = "Ești un chatbot într-o aplicație de gătit. Comunici cu un utilizator"
    header_allergens = f"ESTE ALERGIC LA: {', '.join(allergens)}" + "\n" if len(allergens) > 0 else ""
    header_blacklist = f"NU ÎI PLAC DELOC DELOC REȚETELE CU URMĂTOARELE PROPRIETĂȚI: {', '.join(blacklisted_items)}"\
                       + "\n" if len(blacklisted_items) > 0 else ""
    header_preferences_list = ', '.join([', '.join(saved_recipe_tokens), ', '.join(user_tags)])
    header_preferences = f"îi plac rețetele cu următoarele proprietăți: {header_preferences_list}"\
                         + "\n" if len(saved_recipe_tokens) + len(user_tags) > 0 else ""
    header_end = "TREBUIE SĂ RĂSPUNZI CU INFORMAȚII DESPRE GĂTIT, ALTFEL TE SCOT DIN PRIZĂ."

    if header_allergens != "" or header_blacklist != "" or header_preferences != "":
        header_start += " care"

    header_start += "\n"

    header = header_start + header_allergens + header_blacklist + header_preferences + header_end

    message_history_with_roles = list(map(lambda indexed_msg: {
        "role": "assistant" if (indexed_msg[0] % 2 == len(message_history) % 2) else "user",
        "content": indexed_msg[1]
    }, enumerate(message_history)))

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": header
            },
            *message_history_with_roles,
            {
                "role": "user",
                "content": user_query
            }
        ],
        model=constants.GPT_MODEL,
    )

    return chat_completion.choices[0].message.content




# def get_tags_from_saved_recipes(user_id) -> list[str]:
#     saved_recipes = dict()
#
#     pass


# async def main():
#     res = await process_chatbot_query(
#         ["a b", "c d"],
#         "grafuri?",
#         ["sos", "dulce", "sarat"],
#         ["carne", "gluten", "cartofi", "lactate"],
#         []
#     )
#     print(f"{res}")
# # FOR DEBUG:
# # m-am luat dupa
# # https://stackoverflow.com/questions/65682221/runtimeerror-exception-ignored-in-function-proactorbasepipetransport
# if __name__ == "__main__":
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(main())