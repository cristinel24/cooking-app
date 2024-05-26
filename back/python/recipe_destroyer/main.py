from typing import Annotated

import uvicorn
from fastapi import FastAPI, Header, status
from fastapi.responses import JSONResponse

from constants import *
from services import *

load_dotenv()

app = FastAPI(title="Recipe Destroyer")


@app.delete(
    "/recipe/{recipe_id}",
    tags=["recipe-destroyer"],
    response_model=None,
    response_description="Successful operation"
)
async def delete_recipe(recipe_id: str, x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if x_user_id is None:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": ErrorCodes.UNAUTHENTICATED.value})

    try:
        await delete_recipe_service(recipe_id, x_user_id)
    except RecipeDestroyerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
