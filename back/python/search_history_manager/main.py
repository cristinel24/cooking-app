from fastapi import FastAPI, Response

import json
import services
import constants
import exceptions

app = FastAPI()


@app.get("/user/{user_id}/search-history")
async def get_search_history(user_id: str, start: int, count: int): # returns empty list if no search history is found
    try:
        return await services.get_search_history(user_id, start, count)
    except exceptions.SearchHistoryException as e:
        return Response(status_code=e.status_code,
                        content=json.dumps({"errorCode": e.error_code.value}))


@app.put("/user/{user_id}/search-history")
async def add_search_history(user_id: str, search_query: str): # returns false if search query is not added
    try:
        return await services.add_search_history(user_id, search_query)
    except exceptions.SearchHistoryException as e:
        return Response(status_code=e.status_code,
                        content=json.dumps({"errorCode": e.error_code.value}))


@app.delete("/user/{user_id}/search-history")  # returns false if no search history is cleared
async def clear_search_history(user_id: str):
    try:
        return await services.clear_search_history(user_id)
    except exceptions.SearchHistoryException as e:
        return Response(status_code=e.status_code,
                        content=json.dumps({"errorCode": e.error_code.value}))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=constants.HOST_URL, port=constants.PORT)
