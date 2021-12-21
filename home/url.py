from fastapi import FastAPI, APIRouter
from .views import create_user, users
from .schema import PydanticUser

router = APIRouter(prefix="/home", tags=["home"])

router.post("/create_user/")(create_user)
router.get("/users/", response_model=list[PydanticUser])(users)
