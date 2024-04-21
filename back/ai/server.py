import os
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter

import processor
from utils import schemas

from utils import tokenize_query

load_dotenv()

PORT = int(os.getenv("PORT", "8000"))

app = FastAPI()

router = APIRouter(
    prefix="/api"
)


@router.post("/tokenize/recipe", tags=["tokenize"])
async def tokenize_recipe(recipe: schemas.TokenizeRecipeSchema):
    return await processor.process_recipe(recipe)


@router.get("/tokenize/user_query/{query}", tags=["tokenize"])
async def tokenize_user_query(query):
    return await processor.process_query(query)


@router.post("/chatbot", tags=["chatbot"])
async def process_chatbot_query(query: schemas.ChatbotInput):
    return await processor.process_chatbot(query)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
