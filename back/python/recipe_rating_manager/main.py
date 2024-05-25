from fastapi import FastAPI

from recipe_rating_manager.services import *
from schemas import RatingCreateRequest, RatingUpdateRequest

app = FastAPI(title="Recipe Rating Manager")

# TODO : auth route handling

# PUT ✅
@app.put("/{recipe_id}/ratings", response_model=None, response_description="Successful operation")
async def create_rating(recipe_id: str, rating_data: RatingCreateRequest) -> JSONResponse | None:
    try:
        await put_recipe_services(recipe_id, rating_data)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Rating created successfully"})
    except RecipeRatingManagerException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"errorCode": e.error_code, "message": e.error_message})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.UNKNOWN_ERROR.value, "message": str(e)})

# PATCH ✅
@app.patch("/{recipe_id}/ratings/{rating_id}", response_model=None, response_description="Successful operation")
async def update_rating(recipe_id: str, rating_id: str, rating_data: RatingUpdateRequest) -> JSONResponse| None:
    try:
        await patch_recipe_services(recipe_id, rating_id, rating_data)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Rating updated successfully"})
    except RecipeRatingManagerException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"errorCode": e.error_code, "message": e.error_message})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.UNKNOWN_ERROR.value, "message": str(e)})


# DELETE ✅
@app.delete("/{recipe_id}/ratings/{rating_id}", response_model=None, response_description="Successful operation")
async def delete_rating(recipe_id: str, rating_id: str) -> JSONResponse | None:
    try:
        await delete_recipe_services(recipe_id, rating_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Rating deleted successfully"})
    except RecipeRatingManagerException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"errorCode": e.error_code, "message": e.error_message})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.UNKNOWN_ERROR.value, "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
