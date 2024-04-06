import asyncio
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from processor import gepeto

load_dotenv()

PORT = int(os.getenv('PORT', '8000'))

app = FastAPI()


@app.post('/tokenize/recipe/{id}', summary="", description="")
async def tokenize_recipe():

    return {'message': 'Request on root route!'}


@app.get("/gpt/{query}")
async def test(query):
    return await gepeto(query)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)

