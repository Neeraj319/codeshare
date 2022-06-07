from fastapi.routing import APIRouter
from .views import create_code, create_language

router = APIRouter(prefix="/home", tags=["core"])
router.post('/create_code/')(create_code)
router.post('/create_language/')(create_language)
