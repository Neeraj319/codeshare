from fastapi import APIRouter
from starlette import status
from .views import signup, login, user_detail


router = APIRouter(prefix="/auth", tags=["auth"])

router.post("/signup/")(signup)
router.post(
    "/login/",
    status_code=status.HTTP_201_CREATED,
)(login)
router.get("/user/{user_id}")(user_detail)
