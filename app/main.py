from fastapi import FastAPI
from contextlib import asynccontextmanager
from .config import FILE_PATH
from app.telegram_bot import start_bot

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_bot()
    yield

app = FastAPI(lifespan=lifespan)

# Run with uvicorn app.main:app --reload