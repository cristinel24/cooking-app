from fastapi import FastAPI, HTTPException, status, Response

import services
import constants
import exceptions

from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


@app.get("/user/{user_id}/message-history")
async def get_message_history(user_id: str, start: int, count: int, response: Response):
    try:
        message_history = await services.get_message_history(user_id, start, count)
        if not message_history:
            raise HTTPException(status_code=404, detail="No message history found.")
        return {"message_history": message_history}
    except exceptions.MessageHistoryException as e:
        e.error_code = constants.ErrorCodes.MESSAGE_HISTORY_NOT_FOUND.value
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


@app.put("/user/{user_id}/message-history")
async def add_message_history(user_id: str, message: str, response: Response):
    try:
        success = await services.add_message_history(user_id, message)
        if not success:
            raise HTTPException(status_code=404, detail="Message not added.")
        return {"message": "Message added successfully."}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


@app.delete("/user/{user_id}/message-history")
async def clear_message_history(user_id: str, response: Response):
    try:
        success = await services.clear_message_history(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="No message history to clear.")
        return {"message": "Message history cleared successfully."}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=constants.HOST_URL, port=constants.PORT)
