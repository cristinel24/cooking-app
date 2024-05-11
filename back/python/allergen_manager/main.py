import os
from dotenv import load_dotenv
from fastapi import FastAPI, status, Response
import uvicorn
import services

load_dotenv()

app = FastAPI()


@app.get("/allergen")
async def get_allergens(starting_with: str):
    return services.get_allergens_by_starting_string(starting_with)


@app.post("/allergen/{name}")
async def add_allergen(name: str):
    services.add_allergen_by_name(name)


@app.delete("/allergen/{name}")
async def remove_allergen(name: str, response: Response):
    try:
        services.remove_allergen_by_name(name)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": int(str(e))}


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 8000)))
