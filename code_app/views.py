from fastapi import Depends, HTTPException
from fastapi_pagination import paginate
from code_app import services as code_app_services
from auth import dependencies as auth_dependency
from code_app import schemas as code_app_schemas
from auth import schemas as auth_schemas
from starlette import status
from codeshare import db_init


async def post_code(
    code: code_app_schemas.CodeSchema,
    user: auth_schemas.UserSchema = Depends(auth_dependency.get_user_from_token),
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
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
    if created_code := code_app_services.add_code(
        db_session=db_session, code=code, user=user, language_id=code.language_id
    ):
        db_session.close()
        return created_code
    else:
        db_session.close()
        raise HTTPException(
            detail="language not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def get_code(
    slug: str, db_session: db_init.DBConnector = Depends(db_init.db_connection)
):
    """
    returns code object with the given slug else 404 not found
    """
    if code := code_app_services.get_code_by_slug(db_session=db_session, slug=slug):
        db_session.close()
        return code
    else:
        db_session.close()
        raise HTTPException(
            detail="Code not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def get_all_code(
    user: auth_schemas.UserSchema = Depends(auth_dependency.get_user_from_token),
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
    returns all the code objects related to the particular user
    """
    data = paginate(code_app_services.get_all_from_db(db_session=db_session, user=user))
    db_session.close()
    return data


async def patch_code(
    slug: str,
    code: code_app_schemas.CodeUpdateSchema,
    user: auth_schemas.UserSchema = Depends(auth_dependency.get_user_from_token),
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
        this route updates the particular code object according to the slug passed else 404
        both the fields are optional too
    {
      "text": "string",
      "language_id": int
    }

    """
    if code_from_db := code_app_services.get_code_by_slug(
        db_session=db_session, slug=slug
    ):
        if code_from_db.user_id == user.id:
            if updated_code := code_app_services.update_code(
                db_session=db_session, code=code_from_db, request_data=code
            ):
                db_session.close()
                return updated_code
            raise HTTPException(
                detail="Language not found", status_code=status.HTTP_404_NOT_FOUND
            )
        raise HTTPException(
            detail="you are not allowed to update this code",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    else:
        db_session.close()
        raise HTTPException(
            detail="Code not found", status_code=status.HTTP_404_NOT_FOUND
        )


async def delete_code(
    slug: str,
    user: auth_schemas.UserSchema = Depends(auth_dependency.get_user_from_token),
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
    deletes particular code using the slug from the database
    else if not found 404
    """

    if code_from_db := code_app_services.get_code_by_slug(
        db_session=db_session, slug=slug
    ):
        if code_from_db.user_id == user.id:
            code_app_services.remove_code(db_session=db_session, code=code_from_db)
            db_session.close()
            return {
                "message": "Code deleted successfully",
            }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    else:
        db_session.close()
        raise HTTPException(
            detail="Code not found", status_code=status.HTTP_404_NOT_FOUND
        )
