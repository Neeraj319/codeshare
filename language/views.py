from fastapi import Depends, HTTPException
from admin import dependencies as admin_dependencies
from auth import schemas as auth_schemas
from codeshare import db_init
from language import schemas as language_schemas
from starlette import status
from language import services as language_services


async def post_language(
    language: language_schemas.LanguageSchema,
    user: auth_schemas.UserSchema = Depends(admin_dependencies.get_super_user),
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
        admin specific route, creates passed language to the database
    {
      "name": "string",
    }
    """
    if not user:
        db_session.close()
        raise HTTPException(
            detail="you are not allowed to view this resource",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    created_language = language_services.add_language(
        language=language, user_id=user.id, db_session=db_session
    )
    if not created_language:
        db_session.close()
        raise HTTPException(
            detail="language with that name already exists",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    db_session.close()
    return created_language


# i have not decided yet if i should protect this route or not so
# let's keep it like this for some time


async def get_all_languages(
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
    returns queryset of all languages from the database
    """
    data = language_services.all_languages(db_session=db_session)
    db_session.close()
    return data


async def get_language(
    id: int,
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
    returns language of particular id from the database

    """
    if language := language_services.get_language_fromdb(id=id, db_session=db_session):
        db_session.close()
        return language
    db_session.close()
    raise HTTPException(
        detail="language not found", status_code=status.HTTP_404_NOT_FOUND
    )


async def patch_language(
    id: int,
    language: language_schemas.LanguageUpdateSchema,
    user: auth_schemas.UserSchema = Depends(admin_dependencies.get_super_user),
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
        admin specific route, updates language of particular id from the database
    {
    "name": "string",
    "id": 0
    }
    """
    if not user:
        db_session.close()
        raise HTTPException(
            detail="you are not allowed to view this resource",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if from_db_language := language_services.get_language_fromdb(
        id=id, db_session=db_session
    ):
        language_services.update_language(
            language=from_db_language,
            request_data=language,
            db_session=db_session,
        )
        db_session.close()
        return language
    db_session.close()
    raise HTTPException(
        detail="language not found", status_code=status.HTTP_404_NOT_FOUND
    )


async def delete_language(
    id: int,
    user: auth_schemas.UserSchema = Depends(admin_dependencies.get_super_user),
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
    admin specific route, deletes language of particular id passed
    """

    if not user:
        db_session.close()
        raise HTTPException(
            detail="you are not allowed to view this resource",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if language := language_services.get_language_fromdb(id=id, db_session=db_session):
        language_services.delete_language(language=language, db_session=db_session)
        db_session.close()
        return {"message": "language deleted successfully"}
    db_session.close()
    raise HTTPException(
        detail="language not found", status_code=status.HTTP_404_NOT_FOUND
    )
