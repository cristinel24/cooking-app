import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from services import handle_hash_with_primary_algo, handle_hash_with_specific_algo

load_dotenv()

app = FastAPI()


@app.get("/{target}")
def hash_with_primary_algo(target: str, salt: str | None = None):
    hash_algorithm_name, hashed_target, generated_salt = handle_hash_with_primary_algo(target, salt)
    return {"hashAlgorithmName": hash_algorithm_name, "hash": hashed_target, "salt": generated_salt}


@app.get("/{hash_algorithm_name}/{target}")
def hash_with_specific_algo(hash_algorithm_name: str, target: str, salt: str | None = None):
    hashed_target, generated_salt = handle_hash_with_specific_algo(hash_algorithm_name, target, salt)
    return {"hash": hashed_target, "salt": generated_salt}


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 2020)))
