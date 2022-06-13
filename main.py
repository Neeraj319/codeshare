"""
main part of the application here all whole application unites into this file 
"""

from fastapi import FastAPI
from auth.urls import router
from codeshare.db_init import main, close_db_connection
from admin.urls import router as admin_router
import asyncio
from fastapi_pagination import add_pagination
from code_app.urls import router as code_router
from language.urls import router as language_router

app = FastAPI()
loop = asyncio.get_event_loop()
asyncio.gather(main())
app.include_router(router)
app.include_router(admin_router)
app.include_router(code_router)
app.include_router(language_router)


add_pagination(app)


@app.on_event("shutdown")
def shutdown():
    asyncio.gather(close_db_connection())


@app.get("/")
def home():
    return {"message": "Welcome to CodeShare. Nothing is here go to /docs for more"}
