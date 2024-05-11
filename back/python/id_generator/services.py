from dotenv import load_dotenv
from fastapi import HTTPException
from constants import ERROR_20301
from repository import get_next_id

load_dotenv()

def get_next_id_services() -> str:
    try:
        return get_next_id()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e), headers={ERROR_20301: str(e)})
