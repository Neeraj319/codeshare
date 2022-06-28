from typing import Union
from jose import JWTError, jwt
import os
from auth import services as auth_services
from auth.schemas import UserSchema
from code_app.schemas import CodeSchema
from codeshare import db_init
from fastapi import status, WebSocket
from code_app import services as code_app_services


async def get_code(slug: str, websocket: WebSocket) -> Union[CodeSchema, None]:
    """
    returns code schema object from the database\n
    disconnects if no such code is available

    """
    db_session = db_init.DBConnector()
    from_db = code_app_services.get_code_by_slug(slug=slug, db_session=db_session)
    if not from_db:
        await websocket.close(
            reason="No such code", code=status.WS_1008_POLICY_VIOLATION
        )
        return
    db_session.close()
    return from_db


async def get_user_from_token(token: str) -> Union[UserSchema, None]:
    """
    this dependency is epically for validating if the user is the user\n
    who is associated with the given code object else returns None
    """
    try:
        payload = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=[os.environ.get("ALGORITHM")],
        )
        username: str = payload.get("username")
        if username is None:
            return
    except JWTError:
        return
    db_session = db_init.DBConnector()
    if user := auth_services.get_user_by_username(
        username=username, db_session=db_session
    ):
        db_session.close()
        del user.password
        return user
    else:
        db_session.close()
        return
