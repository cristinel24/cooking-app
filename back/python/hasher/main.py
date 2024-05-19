from fastapi import FastAPI, status, Response
import uvicorn
from constants import HOST, PORT, ErrorCodesToHTTPCodesMapping
from services import handle_hash_with_primary_algo, handle_hash_with_specific_algo

app = FastAPI()


@app.get("/{target}")
async def hash_with_primary_algo(target: str, response: Response, salt: str | None = None):
    try:
        hash_algorithm_name, hashed_target, generated_salt = handle_hash_with_primary_algo(target, salt)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = int(str(e))
        if error_code in ErrorCodesToHTTPCodesMapping:
            response.status_code = ErrorCodesToHTTPCodesMapping[error_code]
        return {"errorCode": error_code}
    return {"hashAlgorithmName": hash_algorithm_name, "hash": hashed_target, "salt": generated_salt}


@app.get("/{hash_algorithm_name}/{target}")
async def hash_with_specific_algo(hash_algorithm_name: str, target: str, response: Response, salt: str | None = None):
    try:
        hashed_target, generated_salt = handle_hash_with_specific_algo(hash_algorithm_name, target, salt)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = int(str(e))
        if error_code in ErrorCodesToHTTPCodesMapping:
            response.status_code = ErrorCodesToHTTPCodesMapping[error_code]
        return {"errorCode": error_code}
    return {"hash": hashed_target, "salt": generated_salt}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
