from fastapi import FastAPI, APIRouter
from .home.url import router

app = FastAPI()
app.include_router(router)
