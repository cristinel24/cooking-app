import ast
import asyncio
import os
from openai import AsyncOpenAI
from pprint import pprint
from dotenv import load_dotenv

from dataclasses import dataclass

load_dotenv()


client = AsyncOpenAI(
    api_key=str(os.getenv("AI_API_KEY", "")),
)


# DEBUG
# if __name__ == "__main__":
#     query = input("Query: ")
#     res = asyncio.run(tokenize_user_query(query))
#     print(f"{query}: {res}")
#     fixed_tokens = asyncio.run(verify_generated_tokens(query, res))
#     print(fixed_tokens)
