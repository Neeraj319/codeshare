from fastapi import Depends, HTTPException
from admin import dependencies as admin_dependencies
from auth.schemas import UserSchema
from .schemas import LanguageSchema
from starlette import status
from language import services as language_services


async def post_language(
    language: LanguageSchema,
    user: UserSchema = Depends(admin_dependencies.get_super_user),
):
    """
        admin specific route, creates passed language to the database
    {
      "name": "string",
    }
    """
    if not user:

        raise HTTPException(
            detail="you are not allowed to view this resource",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    created_language = await language_services.add_language(language=language)
    if not created_language:
        raise HTTPException(
            detail="language with that name already exists",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    return created_language


# i have not decided yet if i should protect this route or not so
# let's keep it like this for some time


async def get_all_languages():
    """
    returns queryset of all languages from the database
    """
    return await language_services.all_languages()


async def get_language(id: int):
    """
    returns language of particular id from the database

    """
    if language := await language_services.get_language_fromdb(id=id):
        return language
    raise HTTPException(
        detail="language not found", status_code=status.HTTP_404_NOT_FOUND
    )


async def patch_language(
    id: int,
    language: LanguageSchema,
    user: UserSchema = Depends(admin_dependencies.get_super_user),
):
    """
        admin specific route, updates language of particular id from the database
    {
    "name": "string",
    "id": 0
    }
    """
    if not user:
        raise HTTPException(
            detail="you are not allowed to view this resource",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if from_db_language := await language_services.non_schema_get_language(id=id):

        await language_services.update_language(
            language=from_db_language, request_data=language
        )
        return language
    raise HTTPException(
        detail="language not found", status_code=status.HTTP_404_NOT_FOUND
    )


async def delete_language(
    id: int, user: UserSchema = Depends(admin_dependencies.get_super_user)
):
    """
    admin specific route, deletes language of particular id passed
    """

    if not user:
        raise HTTPException(
            detail="you are not allowed to view this resource",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if language := await language_services.non_schema_get_language(id=id):
        await language_services.delete_language(language=language)
        return {"message": "language deleted successfully"}
    raise HTTPException(
        detail="language not found", status_code=status.HTTP_404_NOT_FOUND
    )
