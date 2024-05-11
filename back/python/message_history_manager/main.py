from fastapi import FastAPI, HTTPException

import services
from constants import HOST_URL, PORT

from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


@app.get("/user/{user_id}/message-history")
async def get_message_history(user_id: str, start: int, count: int):
    try:
        message_history = await services.get_message_history(user_id, start, count)
        if not message_history:
            raise HTTPException(status_code=404, detail="No message history found.")
        return {"message_history": message_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/user/{user_id}/message-history")
async def add_message_history(user_id: str, message: str):
    try:
        success = await services.add_message_history(user_id, message)
        if not success:
            raise HTTPException(status_code=404, detail="Message not added.")
        return {"message": "Message added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/user/{user_id}/message-history")
async def clear_message_history(user_id: str):
    try:
        success = await services.clear_message_history(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="No message history to clear.")
        return {"message": "Message history cleared successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
