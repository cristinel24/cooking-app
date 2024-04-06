import asyncio
import os
from openai import AsyncOpenAI
from pprint import pprint
from dotenv import load_dotenv

from dataclasses import dataclass

load_dotenv()


client = AsyncOpenAI(
    api_key=str(os.getenv('AI_API_KEY', '')),
)

tokenize_query_header = '''
{
"tags": list
}
genereaza-mi un json la fel ca cel de mai sus. 
INSEREAZA CAT MAI MULTE TAG-URI POSIBILE (cel putin 10) RELVANTE PENTRU O RETETA (PUNE ACCENT PE INGREDIENTE!!!!).

TE ROG SCRIE-MI DOAR JSON!
pentru urmatoarea fraza:
'''


async def gepeto(query) -> dict:
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


