from fastapi import APIRouter
from starlette import status
from .views import create_user, login, users


router = APIRouter(prefix="/home", tags=["users"])

router.post("/signup/")(create_user)
router.get("/users/")(users)
router.post("/login/", status_code=status.HTTP_201_CREATED)(login)
