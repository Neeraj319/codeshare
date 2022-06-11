from fastapi import Depends, HTTPException
from fastapi_pagination import paginate
from code_app import dependencies
from auth import dependencies as auth_dependency
from .schemas import CodeSchema, CodeUpdateSchema
from auth import schemas as auth_schemas
from starlette import status
from admin import dependencies as admin_dependency


async def post_code(
    code: CodeSchema,
    user: auth_schemas.PydanticUser = Depends(auth_dependency.get_user_from_token),
):
    if created_code := await dependencies.add_code(
        code=code, user=user, language_id=code.language_id
    ):
        return created_code
    else:
        raise HTTPException(
            detail="language not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def get_code(slug: str):
    if code := await dependencies.get_code_by_slug(slug=slug):
        return code
    else:
        raise HTTPException(
            detail="Code not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def get_all_code(
    user: auth_schemas.PydanticUser = Depends(admin_dependency.get_super_user),
):
    return paginate(await dependencies.get_all_from_db())


async def patch_code(
    slug: str,
    code: CodeUpdateSchema,
    user: auth_schemas.PydanticUser = Depends(auth_dependency.get_user_from_token),
):
    if code_from_db := await dependencies.get_code_by_slug(slug=slug):
        print(code_from_db)
        if code_from_db.user.id == user.id:
            await dependencies.update_code(code=code_from_db, request_data=code)
            return code
        raise HTTPException(
            detail="you are not allowed to update this code",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    else:
        raise HTTPException(
            detail="Code not found", status_code=status.HTTP_404_NOT_FOUND
        )
