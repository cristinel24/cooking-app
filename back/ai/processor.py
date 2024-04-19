import asyncio
import os
from openai import AsyncOpenAI
from pprint import pprint
from dotenv import load_dotenv

from utils import constants

from dataclasses import dataclass

load_dotenv()


client = AsyncOpenAI(
    api_key=str(os.getenv('AI_API_KEY', '')),
)


async def tokenize_user_query(query: str) -> dict:
    tokenize_query_header = """
        Genereaza-mi DOAR un json cu formatul de mai jos:
        {
        "tags": list
        }
        in care sa pui cat mai multe tag-uri (macar 20) sortate dupa relevanta pentru mesajul scris mai jos.
        Daca mesajul nu are legatura cu domeniul culinar, returneaza "None".
        Nu adauga paranteze cu explicatii la tag-uri. Nu scrie nimic altceva inafara de json.
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
    return eval(chat_completion.choices[0].message.content)


async def verify_generated_tokens(original_prompt: str, generated_tokens: dict) -> dict:
    verification_header = f"""
    Din urmatorul json:
    {generated_tokens}
    elimina tag-urile care nu au legatura directa cu urmatorul mesaj legat de domeniul culinar:
    {original_prompt}
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
    return eval(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    query = input("Query: ")
    res = asyncio.run(tokenize_user_query(query))
    print(f"{query}: {res}")
    fixed_tokens = asyncio.run(verify_generated_tokens(query, res))
    print(fixed_tokens)

