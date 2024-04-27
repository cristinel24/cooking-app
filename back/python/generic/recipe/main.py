import sys
import os
from dotenv import load_dotenv
from fastapi import FastAPI

from generic.recipe.controller import router

###pentru import de module(nu)
sys.path.insert(1, os.path.join(sys.path[0], '..'))


load_dotenv()

PORT = int(os.getenv("PORT", "8082")) 

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)