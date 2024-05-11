from fastapi import FastAPI, HTTPException
from constants import ERROR_20301
from services import get_next_id_services
from dotenv import load_dotenv
import uvicorn
import os

app = FastAPI()

load_dotenv()
PORT = os.getenv("PORT")
print("Port:", PORT)

@app.get("/")
async def get_id():
    try:
        new_id = get_next_id_services()
        return new_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e), headers={ERROR_20301: str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=int(PORT), reload=True)
