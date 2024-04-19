import asyncio
import os
from fastapi import FastAPI
from dotenv import load_dotenv
import processor
from utils import tokenize_query

load_dotenv()

PORT = int(os.getenv("PORT", "8000"))

app = FastAPI()


@app.post("/tokenize/recipe/{id}", summary="", description="")
async def tokenize_recipe():
    return {"message": "Request on root route!"}


@app.get("/gpt/{query}")
async def tokenize_user_query(query):
    return await tokenize_query.verify_generated_tokens(query, await tokenize_query.tokenize_user_query(query))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
