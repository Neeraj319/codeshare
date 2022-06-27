from .manager import ConnectionManager
from fastapi import WebSocket, Depends, WebSocketDisconnect
from .dependencies import get_user_from_token, get_code


sockets = ConnectionManager()


async def edit(
    websocket: WebSocket,
    code: str = Depends(get_code),
    token: str = Depends(get_user_from_token),
):
    if token and code:
        try:
            await websocket.accept()

            while True:
                data = await websocket.receive_text()
                print(data)
                await websocket.send_json({})
        except WebSocketDisconnect:
            ...
