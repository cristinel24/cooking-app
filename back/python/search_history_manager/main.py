from fastapi import FastAPI

from fastapi.responses import JSONResponse
from schemas import History, Search
import services
import constants
import exceptions

app = FastAPI(title="Search History Manager")


@app.get("/{user_id}/search-history", response_model=History, response_description="Successful operation")
async def get_search_history(user_id: str, start: int, count: int) -> History | JSONResponse:
    try:
        search_history_list = await services.get_search_history(user_id, start, count)
        return History(history=search_history_list)
    except exceptions.SearchHistoryException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


@app.post("/{user_id}/search-history", response_model=None, response_description="Successful operation")
async def add_search_history(user_id: str, body: Search) -> None | JSONResponse:
    try:
        await services.add_search_history(user_id, body.search)
    except exceptions.SearchHistoryException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


@app.delete("/{user_id}/search-history", response_model=None, response_description="Successful operation")
async def clear_search_history(user_id: str) -> None | JSONResponse:
    try:
        await services.clear_search_history(user_id)
    except exceptions.SearchHistoryException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=constants.HOST, port=constants.PORT)
