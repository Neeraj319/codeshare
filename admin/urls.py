from fastapi import APIRouter
from starlette import status
from admin import views
from fastapi_pagination import Page
from auth.schemas import UserResponseSchema
from code_app import schemas as code_schema

router = APIRouter(prefix="/admin", tags=["admin"])

router.post("/create_user/", status_code=status.HTTP_201_CREATED)(views.create_user)
router.get("/users/", response_model=Page[UserResponseSchema])(views.users)
router.delete("/users/{username}/", status_code=status.HTTP_200_OK)(views.delete_user)
router.patch("/users/{username}/", status_code=status.HTTP_200_OK)(views.patch_user)
router.get(
    "/code/",
    response_model=Page[code_schema.CodeSchema],
)(views.get_all_code)
