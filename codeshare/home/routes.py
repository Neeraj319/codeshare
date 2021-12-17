from fastapi import FastAPI, APIRouter
from .views import main

router = APIRouter(prefix="/home", tags=["home"])

router.get("/")(main)
