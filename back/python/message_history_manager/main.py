from fastapi import FastAPI

from fastapi.responses import JSONResponse
from schemas import History, Message
import services
import constants
import exceptions

app = FastAPI(title="Message History Manager")


@app.get("/{user_id}/message-history", response_model=History, response_description="Successful operation")
async def get_message_history(user_id: str, start: int, count: int) -> History | JSONResponse:
    try:
        history =  await services.get_message_history(user_id, start, count)
        return History(history=history)
    except exceptions.MessageHistoryException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


@app.post("/{user_id}/message-history", response_model=None, response_description="Successful operation")
async def add_message_history(user_id: str, body: Message) -> None | JSONResponse:
    try:
        await services.add_message_history(user_id, body.message)
    except exceptions.MessageHistoryException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


@app.delete("/{user_id}/message-history", response_model=None, response_description="Successful operation")
async def clear_message_history(user_id: str) -> None | JSONResponse:
    try:
        await services.clear_message_history(user_id)
    except exceptions.MessageHistoryException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=constants.HOST, port=constants.PORT)
