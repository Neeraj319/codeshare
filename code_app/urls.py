from fastapi.routing import APIRouter
from starlette import status
from .views import post_code

router = APIRouter(prefix="/code", tags=["code"])

# router.post('/add/')(create_code)
router.post(
    '/add/', status_code=status.HTTP_201_CREATED
)(post_code)
