from fastapi import APIRouter
from starlette import status
from .views import create_user,  users
from fastapi_pagination import Page
from auth.schema import PydanticUserResponseModel
router = APIRouter(prefix="/admin", tags=["admin"])

router.post("/create_user/", status_code=status.HTTP_201_CREATED)(create_user)
router.get("/users/", response_model=Page[PydanticUserResponseModel])(users)
