from fastapi import FastAPI, APIRouter
from .views import create_user

router = APIRouter(prefix="/home", tags=["home"])

router.get("/")(create_user)
