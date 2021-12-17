from fastapi import FastAPI, APIRouter
from .home import routes

app = FastAPI()
app.include_router(router=routes.router)
