from typing import Annotated

from fastapi import FastAPI, status
from fastapi.params import Header
from fastapi.responses import JSONResponse

import services
from constants import HOST, PORT, ErrorCodes
from exception import RecipeCreatorException
from schemas import RecipeData

app = FastAPI(title="Recipe Creator")


@app.post("/", response_model=None, response_description="Successful operation")
async def create_recipe(recipe_data: RecipeData,
                        x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": ErrorCodes.NOT_AUTHENTICATED.value})
    try:
        await services.create_recipe(x_user_id, recipe_data)
    except RecipeCreatorException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
