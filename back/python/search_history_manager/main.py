from fastapi import FastAPI 

from fastapi.responses import JSONResponse
from schemas import History
import services
import constants
import exceptions

app = FastAPI(title="Search History Manager")


@app.get("/{user_id}/search-history", response_model=History, response_description="Successful operation")
async def get_search_history(user_id: str, start: int, count: int) -> History | JSONResponse:  # returns empty list if no search history is found
    try:
        return await services.get_search_history(user_id, start, count)
    except exceptions.SearchHistoryException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


@app.put("/{user_id}/search-history", response_model=None, response_description="Successful operation")
async def add_search_history(user_id: str, search_query: str) -> None | JSONResponse:  # returns false if search query is not added
    try:
        await services.add_search_history(user_id, search_query)
    except exceptions.SearchHistoryException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


@app.delete("/{user_id}/search-history", response_model=None, response_description="Successful operation")
async def clear_search_history(user_id: str) -> None | JSONResponse: # returns false if no search history is cleared
    try:
        await services.clear_search_history(user_id)
    except exceptions.SearchHistoryException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=constants.HOST, port=constants.PORT)
