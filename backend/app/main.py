from fastapi import FastAPI
import uvicorn

from core.config import config
from src.head_router import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT
    )