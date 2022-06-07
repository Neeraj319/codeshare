from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status
from fastapi import Request
from .schema import CodeSchema, LanguageSchema
from auth.dependencies import get_user_from_token
from admin.dependencies import get_super_user
from auth.schema import PydanticUser


async def create_code(code: CodeSchema, user: PydanticUser = Depends(get_user_from_token)):
    ...


async def create_language(language: LanguageSchema, admin_user: PydanticUser = Depends(get_super_user)):

    if admin_user:
        return {
            'status': "ok"
        }
    else:
        raise HTTPException(
            detail="you are not authorized to access this resource",
            status_code=status.HTTP_403_FORBIDDEN,
        )
