import os
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter

import processor
from utils import tokenize_query, schemas
from utils import process_chatbot

load_dotenv()

PORT = int(os.getenv("PORT", "8000"))

app = FastAPI()

router = APIRouter(
    prefix="/api"
)


@router.post("/tokenize/recipe", tags=["tokenize"])
async def tokenize_recipe():
    return {"message": "Request on root route!"}


@router.get("/tokenize/user_query/{query}", tags=["tokenize"])
async def tokenize_user_query(query):
    return await tokenize_query.verify_generated_tokens(query, await tokenize_query.tokenize_user_query(query))


@router.post("/chatbot", tags=["chatbot"])
async def process_chatbot_query(query: schemas.ChatbotInput):
    return await process_chatbot.process_chatbot(query)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
