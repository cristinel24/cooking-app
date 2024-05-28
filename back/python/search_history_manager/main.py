from typing import Annotated

from fastapi import FastAPI, Header, status
from fastapi.responses import JSONResponse

import exceptions
import services
from constants import HOST, PORT, ErrorCodes
from schemas import History, Search
from utils import get_error_json_response

app = FastAPI(title="Search History Manager")


@app.get("/{user_id}/search-history", response_model=History, response_description="Successful operation")
async def get_search_history(user_id: str, start: int, count: int,
                             x_user_id: Annotated[str | None, Header()] = None) -> History | JSONResponse:
    if not x_user_id:
        return get_error_json_response(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHORIZED_REQUEST)

    if x_user_id != user_id:
        return get_error_json_response(status.HTTP_403_FORBIDDEN, ErrorCodes.FORBIDDEN_REQUEST)

    try:
        search_history_list = await services.get_search_history(user_id, start, count)
        return History(history=search_history_list)
    except exceptions.SearchHistoryException as e:
        return get_error_json_response(e.status_code, e.error_code)


@app.put("/{user_id}/search-history", response_model=None, response_description="Successful operation")
async def add_search_history(user_id: str, body: Search,
                             x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id:
        return get_error_json_response(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHORIZED_REQUEST)

    if x_user_id != user_id:
        return get_error_json_response(status.HTTP_403_FORBIDDEN, ErrorCodes.FORBIDDEN_REQUEST)

    try:
        await services.add_search_history(user_id, body.search)
    except exceptions.SearchHistoryException as e:
        return get_error_json_response(e.status_code, e.error_code)


@app.delete("/{user_id}/search-history", response_model=None, response_description="Successful operation")
async def clear_search_history(user_id: str, x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id:
        return get_error_json_response(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHORIZED_REQUEST)

    if x_user_id != user_id:
        return get_error_json_response(status.HTTP_403_FORBIDDEN, ErrorCodes.FORBIDDEN_REQUEST)

    try:
        await services.clear_search_history(user_id)
    except exceptions.SearchHistoryException as e:
        return get_error_json_response(e.status_code, e.error_code)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
