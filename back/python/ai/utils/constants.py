import os

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
AI_API_KEY = str(os.getenv("AI_API_KEY", ""))

GPT_MODEL = "gpt-3.5-turbo"
