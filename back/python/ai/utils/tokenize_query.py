import ast

import constants
from .openai_client import openai_client

client = openai_client()


async def tokenize_user_query(query: str) -> str:
    """
    Return tags relevant to user query.
    :param query: user query
    :return: GPT response with tags relevant to query
    """
    tokenize_query_header = """
        Generează DOAR un JSON cu formatul de mai jos:
        {
        "tags": list of tags
        }
        în care să pui cât mai multe tag-uri (măcar 20) în limba română, sortate după relevanța pentru mesajul de mai jos.
        Nu adăuga NIMIC altceva înafară de JSON.
    """

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{tokenize_query_header} {query}",
            }
        ],
        model=constants.GPT_MODEL,
    )
    return chat_completion.choices[0].message.content


async def verify_generated_tokens(generated_response: str) -> dict:
    """
    Check tags returned by GPT, returning them as a valid dictionary.
    :param generated_response: response generated by GPT
    :return: a dictionary with tags relevant to user query
    """

    tokens_dict = convert_to_dict(generated_response)

    verification_header = f"""
    Din acest JSON, scoate tag-urile care nu au legătură cu domeniul culinar (pot rămâne 0 tag-uri).
    Returnează doar noul JSON, nimic altceva.
    {tokens_dict}
    """
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": verification_header
            }
        ],
        model=constants.GPT_MODEL,
    )
    return convert_to_dict(chat_completion.choices[0].message.content)


def convert_to_dict(text: str) -> dict:
    try:
        dictionary = ast.literal_eval(text)
    except (SyntaxError, ValueError, OverflowError):
        return {"tags": []}

    if not isinstance(dictionary, dict):
        return {"tags": []}

    if list(dictionary.keys()) != ["tags"] or not isinstance(dictionary["tags"], list):
        return {"tags": []}

    if not all(isinstance(tag, str) for tag in dictionary["tags"]):
        return {"tags": []}

    return dictionary


def normalise_dict(dictionary: dict) -> list[str]:
    normalised_tags = []
    for tag in dictionary["tags"]:
        if tag.lower() not in normalised_tags:
            normalised_tags.append(tag.lower())

    return normalised_tags
