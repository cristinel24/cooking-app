import ast
import asyncio
import os
from openai import AsyncOpenAI
from pprint import pprint
from dotenv import load_dotenv
from processor import client

from dataclasses import dataclass


async def tokenize_user_query(query: str) -> str:
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
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content


async def verify_generated_tokens(original_prompt: str, generated_response: str) -> dict:
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
        model="gpt-3.5-turbo",
    )
    try:
        dictionary = ast.literal_eval(chat_completion.choices[0].message.content)
    except (SyntaxError, ValueError, OverflowError):
        return {"eroare": "nu este dictionar"}

    if not isinstance(dictionary, dict):
        return {"eroare": "nu este dictionar"}

    return dictionary
