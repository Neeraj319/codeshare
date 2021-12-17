from fastapi import FastAPI, APIRouter
from .routers import routes

app = FastAPI()
app.include_router(router=routes.router)
