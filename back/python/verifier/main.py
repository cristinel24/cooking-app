from dotenv import load_dotenv
from fastapi import FastAPI, Response
import services
import uvicorn
from constants import HOST, PORT
from exception import VerifierException

app = FastAPI()

load_dotenv()


@app.post("/", tags=["verify"])
async def verify(token_value: str, response: Response) -> dict[str, int] | None:
    try:
        await services.verify(token_value)
    except VerifierException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
