from fastapi import Depends, HTTPException
from .dependencies import add_code
from auth import dependencies as auth_dependency
from .schemas import CodeSchema
from auth import schemas as auth_schemas
from starlette import status


async def post_code(code: CodeSchema, user: auth_schemas.PydanticUser = Depends(auth_dependency.get_user_from_token)):
    if created_code := await add_code(code=code, user=user, language_id=code.language_id):
        return created_code
    else:
        raise HTTPException(
            detail='language not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
