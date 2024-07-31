from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.telegram_bot import start_bot

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_bot()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def hello_fly():
    return 'telegram-cms: https://github.com/daliendev/telegram-cms'