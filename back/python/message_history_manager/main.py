from typing import Annotated

from fastapi import FastAPI, Header, status
from fastapi.responses import JSONResponse

import exceptions
import services
from constants import ErrorCodes, HOST, PORT
from schemas import History, Message
from utils import get_error_json_response

app = FastAPI(title="Message History Manager")


@app.get("/{user_id}/message-history", response_model=History, response_description="Successful operation")
async def get_message_history(user_id: str, start: int, count: int,
                              x_user_id: Annotated[str | None, Header()] = None) -> History | JSONResponse:
    if not x_user_id:
        return get_error_json_response(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHORIZED_REQUEST)

    if x_user_id != user_id:
        return get_error_json_response(status.HTTP_403_FORBIDDEN, ErrorCodes.FORBIDDEN_REQUEST)

    try:
        history = await services.get_message_history(user_id, start, count)
        return History(history=history)
    except exceptions.MessageHistoryException as e:
        return get_error_json_response(e.status_code, e.error_code)


@app.put("/{user_id}/message-history", response_model=None, response_description="Successful operation")
async def add_message_history(user_id: str, body: Message,
                              x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id:
        return get_error_json_response(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHORIZED_REQUEST)

    if x_user_id != user_id:
        return get_error_json_response(status.HTTP_403_FORBIDDEN, ErrorCodes.FORBIDDEN_REQUEST)

    try:
        await services.add_message_history(user_id, body.message)
    except exceptions.MessageHistoryException as e:
        return get_error_json_response(e.status_code, e.error_code)


@app.delete("/{user_id}/message-history", response_model=None, response_description="Successful operation")
async def clear_message_history(user_id: str, x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id:
        return get_error_json_response(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHORIZED_REQUEST)

    if x_user_id != user_id:
        return get_error_json_response(status.HTTP_403_FORBIDDEN, ErrorCodes.FORBIDDEN_REQUEST)

    try:
        await services.clear_message_history(user_id)
    except exceptions.MessageHistoryException as e:
        return get_error_json_response(e.status_code, e.error_code)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
