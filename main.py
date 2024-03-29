"""
main part of the application here all whole application unites into this file 
"""
from fastapi import FastAPI
from auth.urls import router as auth_router
from admin.urls import router as admin_router
import asyncio
from fastapi_pagination import add_pagination
from sockets import main as sockets_main
from code_app.urls import router as code_router
from language.urls import router as language_router
import dotenv

dotenv.load_dotenv()


app = FastAPI(
    title="CodeShare",
)
loop = asyncio.get_event_loop()
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(code_router)
app.include_router(language_router)
app.websocket("/ws/edit/{slug}/{token}/")(sockets_main.edit)
add_pagination(app)


@app.get("/")
# defining home function
def home():

    return {"message": "Welcome to CodeShare. Nothing is here go to /docs for more"}
