from fastapi.routing import APIRouter
from fastapi_pagination import Page
from starlette import status
from code_app.schemas import CodeSchema
from code_app import views

router = APIRouter(prefix="/code", tags=["code"])

router.post(
    "/add/",
    status_code=status.HTTP_201_CREATED,
)(views.post_code)
router.get(
    "/all/",
    response_model=Page[CodeSchema],
)(views.get_all_code)

router.get(
    "/{slug}/",
    status_code=status.HTTP_200_OK,
)(views.get_code)

router.patch(
    "/{slug}/",
    status_code=status.HTTP_200_OK,
)(views.patch_code)
router.delete(
    "/{slug}/",
    status_code=status.HTTP_200_OK,
)(views.delete_code)
