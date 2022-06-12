from fastapi import APIRouter
from starlette import status
from .views import create_user, users, delete_user
from fastapi_pagination import Page
from auth.schemas import PydanticUserResponseModel

router = APIRouter(prefix="/admin", tags=["admin"])

router.post("/create_user/", status_code=status.HTTP_201_CREATED)(create_user)
router.get("/users/", response_model=Page[PydanticUserResponseModel])(users)
router.delete("/users/{user_id}/", status_code=status.HTTP_200_OK)(delete_user)
