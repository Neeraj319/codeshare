from fastapi.routing import APIRouter
from fastapi_pagination import Page
from starlette import status

from code_app.schemas import CodeSchema
from .views import get_all_code, patch_code, post_code, get_code

router = APIRouter(prefix="/code", tags=["code"])

router.post(
    "/add/",
    status_code=status.HTTP_201_CREATED,
)(post_code)
router.get(
    "/all/",
    response_model=Page[CodeSchema],
)(get_all_code)

router.get(
    "/{slug}/",
    status_code=status.HTTP_200_OK,
)(get_code)

router.patch(
    "/{slug}/",
    status_code=status.HTTP_200_OK,
)(patch_code)
