"""
main part of the application here all whole application unites into this file 
"""

from fastapi import FastAPI
from auth.urls import router as auth_router
from fastapi import Depends
from admin.urls import router as admin_router
import asyncio
from fastapi_pagination import add_pagination

from code_app.urls import router as code_router
from language.urls import router as language_router


app = FastAPI(
    title="CodeShare",
)
loop = asyncio.get_event_loop()
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(code_router)
app.include_router(language_router)


add_pagination(app)


@app.get("/")
def home():

    return {"message": "Welcome to CodeShare. Nothing is here go to /docs for more"}
