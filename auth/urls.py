from fastapi import APIRouter
from starlette import status
from auth import views

router = APIRouter(prefix="/auth", tags=["auth"])

router.post("/signup/")(views.signup)
router.post("/login/", status_code=status.HTTP_201_CREATED)(views.login)
router.get("/user/{username}")(views.user_detail)
router.post("/redis/", status_code=status.HTTP_201_CREATED)(views.create_token_sockets)
router.get("/redis/{token}/")(views.check_socket_token)
