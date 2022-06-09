from fastapi.routing import APIRouter
# from .views import create_code, create_language

router = APIRouter(prefix="/code", tags=["code"])
# router.post('/add/')(create_code)
