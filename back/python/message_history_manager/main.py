from fastapi import FastAPI, Response

import json
import services
import constants
import exceptions

app = FastAPI()


@app.get("/user/{user_id}/message-history")
async def get_message_history(user_id: str, start: int, count: int):
    try:
        return await services.get_message_history(user_id, start, count)
    except exceptions.MessageHistoryException as e:
        return Response(status_code=e.status_code,
                        content=json.dumps({"errorCode": e.error_code.value}))


@app.put("/user/{user_id}/message-history")
async def add_message_history(user_id: str, message: str):
    try:
        return await services.add_message_history(user_id, message)
    except exceptions.MessageHistoryException as e:
        return Response(status_code=e.status_code,
                        content=json.dumps({"errorCode": e.error_code.value}))


@app.delete("/user/{user_id}/message-history")
async def clear_message_history(user_id: str):
    try:
        return  await services.clear_message_history(user_id)
    except exceptions.MessageHistoryException as e:
        return Response(status_code=e.status_code,
                        content=json.dumps({"errorCode": e.error_code.value}))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=constants.HOST_URL, port=constants.PORT)
