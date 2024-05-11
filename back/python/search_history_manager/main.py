from fastapi import FastAPI, Response

import services
from constants import HOST_URL, PORT

app = FastAPI()


@app.get("/user/{user_id}/search-history")  # cannot use ?start={start}&count={count}
async def get_search_history(user_id: str, start: int, count: int):
    return await services.get_search_history(user_id, start, count)


@app.put("/user/{user_id}/search-history")
async def add_search_history(user_id: str, search_query: str):
    return await services.add_search_history(user_id, search_query)


@app.delete("/user/{user_id}/search-history")
async def clear_search_history(user_id: str):
    return await services.clear_search_history(user_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
