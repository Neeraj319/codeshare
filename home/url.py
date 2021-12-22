from fastapi import FastAPI, APIRouter
from starlette import status
from .views import create_user, login, users
from .schema import PydanticUser

router = APIRouter(prefix="/home", tags=["users"])

router.post("/create_user/")(create_user)
router.get("/users/")(users)
router.post("/login/", status_code=status.HTTP_201_CREATED)(login)
