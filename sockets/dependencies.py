from typing import Union
import os
import redis
from auth.schemas import UserSchema
from code_app.schemas import CodeSchema
from codeshare import db_init
from fastapi import status, WebSocket
from code_app import services as code_app_services
from auth import services as auth_services


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


async def get_user_from_token(
    token: str,
) -> Union[UserSchema, None]:
    """
    this dependency is epically for validating if the user is the user\n
    who is associated with the given token object else returns None
    """
    redis_client = redis.Redis(
        host=os.environ.get("REDIS_HOST"),
        port=os.environ.get("REDIS_PORT"),
        password=os.environ.get("REDIS_PASSWORD"),
    )
    token_id = redis_client.get(token)
    if token_id:
        token_id = int(token_id.decode())
        db_session = db_init.db_connection()
        if user := auth_services.get_user_by_id(
            user_id=int(token_id), db_session=db_session
        ):
            db_session.close()
            return user
        db_session.close()
