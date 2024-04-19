import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

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
