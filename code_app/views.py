from fastapi import Depends, HTTPException
from fastapi_pagination import paginate
from code_app import dependencies as code_app_dependencies
from auth import dependencies as auth_dependency
from code_app import schemas as code_app_schemas
from auth import schemas as auth_schemas
from starlette import status


async def post_code(
    code: code_app_schemas.CodeSchema,
    user: auth_schemas.UserSchema = Depends(auth_dependency.get_user_from_token),
):
    """
        adds the given code to the database\n
        user must be authenticated to use this route

    {
      'text': 'string',\n
      'language_id': int,
    }
    """
    # check fro language with given id is necessary
    if created_code := await code_app_dependencies.add_code(
        code=code, user=user, language_id=code.language_id
    ):
        return created_code
    else:
        raise HTTPException(
            detail="language not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def get_code(slug: str):
    """
    returns code object with the given slug else 404 not found
    """
    if code := await code_app_dependencies.get_code_by_slug(slug=slug):
        return code
    else:
        raise HTTPException(
            detail="Code not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def get_all_code(
    user: auth_schemas.UserSchema = Depends(auth_dependency.get_user_from_token),
):
    """
    returns all the code objects related to the particular user
    """
    return paginate(await code_app_dependencies.get_all_from_db(user=user))


async def patch_code(
    slug: str,
    code: code_app_schemas.CodeUpdateSchema,
    user: auth_schemas.UserSchema = Depends(auth_dependency.get_user_from_token),
):
    """
        this route updates the particular code object according to the slug passed else 404
        both the fields are optional too
    {
      "text": "string",
      "language_id": int
    }

    """
    if code_from_db := await code_app_dependencies.get_code_by_slug(slug=slug):

        if code_from_db.user_id == user.id:
            return await code_app_dependencies.update_code(
                code=code_from_db, request_data=code
            )
        raise HTTPException(
            detail="you are not allowed to update this code",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    else:
        raise HTTPException(
            detail="Code not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def delete_code(
    slug: str,
    user: auth_schemas.UserSchema = Depends(auth_dependency.get_user_from_token),
):
    """
    deletes particular code using the slug from the database
    else if not found 404
    """

    if code_from_db := await code_app_dependencies.get_code_by_slug(slug=slug):
        if code_from_db.user_id == user.id:
            await code_app_dependencies.remove_code(code=code_from_db)
            return {
                "message": "Code deleted successfully",
            }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    else:
        raise HTTPException(
            detail="Code not found", status_code=status.HTTP_404_NOT_FOUND
        )
