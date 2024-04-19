import asyncio
import os
from fastapi import FastAPI
from dotenv import load_dotenv
import processor

load_dotenv()

PORT = int(os.getenv('PORT', '8000'))

app = FastAPI()


@app.post('/tokenize/recipe/{id}', summary="", description="")
async def tokenize_recipe():
    return {'message': 'Request on root route!'}


@app.get("/gpt/{query}")
async def tokenize_user_query(query):
    return await processor.verify_generated_tokens(query, await processor.tokenize_user_query(query))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
