from starlette import status
from fastapi.routing import APIRouter
from language import views
router = APIRouter(prefix="/language", tags=["language"])
router.post('/add/',
            status_code=status.HTTP_201_CREATED,
            )(views.post_language)
router.get(
    '/all/',
    status_code=status.HTTP_200_OK,
)(views.get_all_languages)
