from fastapi import FastAPI
from fastapi.responses import JSONResponse
import services
import uvicorn
from constants import HOST, PORT
from exception import VerifierException

app = FastAPI(title="Verifier")


@app.post("/", tags=["verify"], response_model=None, response_description="Successful operation")
async def verify(token_value: str) -> dict[str, int] | None | JSONResponse:
    try:
        await services.verify(token_value)
    except VerifierException as e:
        return JSONResponse(status_code=e.status_code, content={"error_code": e.error_code})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
