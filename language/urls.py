from starlette import status
from fastapi.routing import APIRouter
from language import views

router = APIRouter(prefix="/language", tags=["language"])
router.post(
    "/add/",
    status_code=status.HTTP_201_CREATED,
)(views.post_language)
router.get(
    "/all/",
    status_code=status.HTTP_200_OK,
)(views.get_all_languages)

router.get(
    "/{id}/",
    status_code=status.HTTP_200_OK,
)(views.get_language)

router.patch(
    "/{id}/",
    status_code=status.HTTP_200_OK,
)(views.patch_language)

router.delete(
    "/{id}/",
    status_code=status.HTTP_200_OK,
)(views.delete_language)
