from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

import services
from constants import PORT, ErrorCodes, HOST
from exceptions import AIException
from schemas import *

app = FastAPI(title="AI")


@app.post(
    "/tokenize/recipe",
    response_model=GeneratedTokens,
    response_description="Successful operation",
    tags=["tokenize"]
)
async def tokenize_recipe(recipe: RecipeData) -> GeneratedTokens | JSONResponse:
    try:
        tokens = await services.process_recipe(recipe)
        return GeneratedTokens(tokens=tokens)
    except AIException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"errorCode": ErrorCodes.UNKNOWN.value}
        )


@app.post(
    "/tokenize/replace_ingredient",
    response_model=ReplaceIngredientsList,
    response_description="Successful operation",
    tags=["tokenize"]
)
async def replace_ingredient(request_data: ReplaceIngredientData) -> ReplaceIngredientsList | JSONResponse:
    try:
        # TODO: DECIDE IF WE'LL IMPLEMENT IT OR NOT
        # ingredients = await services.replace_ingredient(request_data)
        return ReplaceIngredientsList(replaceOptions=[request_data.ingredient])
    except AIException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"errorCode": ErrorCodes.UNKNOWN.value}
        )


@app.get(
    "/tokenize/user_query",
    response_model=GeneratedTokens,
    response_description="Successful operation",
    tags=["tokenize"]
)
async def tokenize_user_query(query: str) -> GeneratedTokens | JSONResponse:
    try:
        tokens = await services.process_query(query)
        return GeneratedTokens(tokens=tokens)
    except AIException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"errorCode": ErrorCodes.UNKNOWN.value}
        )


@app.post("/chatbot", response_model=ChatbotResponse, response_description="Successful operation", tags=["chatbot"])
async def process_chatbot_query(query: ChatbotInput) -> ChatbotResponse | JSONResponse:
    try:
        response = await services.process_chatbot(query)
        return ChatbotResponse(response=response)
    except AIException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"errorCode": ErrorCodes.UNKNOWN.value}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
