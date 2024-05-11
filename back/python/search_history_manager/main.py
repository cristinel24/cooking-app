from fastapi import FastAPI, Response, status, HTTPException

import services
import constants
import exceptions

app = FastAPI()


@app.get("/user/{user_id}/search-history")
async def get_search_history(user_id: str, start: int, count: int, response: Response):
    try:
        history = await services.get_search_history(user_id, start, count)
        if not history:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No search history found")
        return history
    except exceptions.SearchHistoryException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": e.error_code, "message": e.message}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value, "message": str(e)}


@app.put("/user/{user_id}/search-history")
async def add_search_history(user_id: str, search_query: str, response: Response):
    try:
        return await services.add_search_history(user_id, search_query)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


@app.delete("/user/{user_id}/search-history")  # retuns false if no search history is found
async def clear_search_history(user_id: str, response: Response):
    try:
        return await services.clear_search_history(user_id)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=constants.HOST_URL, port=constants.PORT)
