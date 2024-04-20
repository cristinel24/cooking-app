import ast

from processor import client
from . import constants


async def tokenize_user_query(query: str) -> str:
    """
    Return tags relevant to user query.
    :param query: user query
    :return: GPT response with tags relevant to query
    """
    tokenize_query_header = """
        Genereaza DOAR un JSON cu formatul de mai jos:
        {
        "tags": list
        }
        in care sa pui cat mai multe tag-uri (macar 20) in limba romana sortate dupa relevanta pentru mesajul de mai jos.
        Nu adauga NIMIC altceva inafara de JSON.
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


async def verify_generated_tokens(original_prompt: str, generated_response: str) -> dict:
    """
    Check tags returned by GPT, returning them as a valid dictionary.
    :param original_prompt: original user query
    :param generated_response: response generated by GPT
    :return: a dictionary with tags relevant to user query
    """
    verification_header = f"""Din urmatorul TEXT:
    
    TEXT = "{generated_response}"
    
    Daca nu este JSON, returneaza cuvantul "None"
    Daca este JSON, elimina toate tag-urile care nu au DELOC LEGATURA CU DOMENIUL CULINAR.
    Apoi, elimina toate tag-urile care nu au DELOC LEGATURA cu urmatorul INPUT:
    
    INPUT = "{original_prompt}"
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
    try:
        dictionary = ast.literal_eval(chat_completion.choices[0].message.content)
    except (SyntaxError, ValueError, OverflowError):
        return {"eroare": "nu este dictionar"}

    if not isinstance(dictionary, dict):
        return {"eroare": "nu este dictionar"}

    return dictionary
