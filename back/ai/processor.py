import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from utils.db_wrapper import DBWrapper

load_dotenv()

db_wrapper = DBWrapper()

client = AsyncOpenAI(
    api_key=str(os.getenv("AI_API_KEY", "")),
)