from fastapi import FastAPI, APIRouter
from .views import create_user, users

router = APIRouter(prefix="/home", tags=["home"])

router.post("/create_user/")(create_user)
router.get("/users/")(users)
