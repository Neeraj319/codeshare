import asyncio
from redis import Redis
from .manager import ConnectionManager, CustomWebSocket
from fastapi import Depends, WebSocketDisconnect
from .dependencies import get_user_from_token, get_code
from codeshare import db_init
from code_app import services as code_app_services
from code_app import schemas as code_app_schemas

sockets = ConnectionManager()


async def edit(
    websocket: CustomWebSocket,
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
    code: str = Depends(get_code),
    token: str = Depends(get_user_from_token),
):
    if token and token.id == code.user_id:
        user_type = "editor"
    else:
        user_type = "viewer"
    websocket.user_type = user_type
    room = await sockets.connect(websocket)
    redis_client: Redis = room.redis_client
    if not (text := redis_client.hget(code.slug, "text")):
        redis_client.hset(code.slug, "text", code.text)
        text = redis_client.hget(code.slug, "text")
    await sockets.send_personal_message(
        {"user_type": user_type, "text": text.decode()}, websocket
    )
    try:
        while True:
            message = await websocket.receive_json()
            if websocket.user_type == "editor":
                await sockets.broadcast(message, code.slug)
                await asyncio.sleep(0.5)
                redis_client.hset(code.slug, "text", message["text"])
    except WebSocketDisconnect:
        if websocket.user_type == "editor":
            updated_code = code_app_schemas.CodeUpdateSchema(
                text=redis_client.hget(code.slug, "text").decode()
            )
            code_app_services.update_code(
                code=code, db_session=db_session, request_data=updated_code
            )
            db_session.close()
        await sockets.disconnect(websocket)
