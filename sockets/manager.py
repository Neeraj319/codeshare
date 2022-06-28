from fastapi import WebSocket
from typing import List, Union
import os
import redis


class Editor:
    """
    Class to represent Editor
    """


class Viewer:
    """
    Class to represent Viewer
    """


class CustomWebSocket(WebSocket):

    # to represent the type of user
    user_type: Union[None, Union[Editor, Viewer]] = None


class Room:
    """
    Class that holds information of a particular code for sharing

    """

    def __init__(self) -> None:
        self.editor: CustomWebSocket = None
        self.redis_client: redis.Redis = redis.Redis(
            host=os.environ.get("REDIS_HOST"),
            port=os.environ.get("REDIS_PORT"),
            password=os.environ.get("REDIS_PASSWORD"),
        )
        self.viewers: List[CustomWebSocket] = []

    def set_user(self, socket: CustomWebSocket):
        if socket.user_type == "editor":
            self.editor = socket
        else:
            self.viewers.append(socket)

    def change_user(self, socket: CustomWebSocket):
        if socket.user_type == "editor":
            self.editor = None
        else:
            self.viewers.remove(socket)

    async def broadcast_message(self, message: dict):
        if self.viewers is not None:
            for viewer in self.viewers:
                await viewer.send_json(message)


class ConnectionManager:
    """
    Main class for handling multiple client WebSocket requests
    """

    def __init__(self):
        self.active_connections: List[CustomWebSocket] = []
        self.groups = {}  # i have no ideaa wh

    async def connect(self, websocket: CustomWebSocket) -> Room:
        await websocket.accept()
        code_slug = websocket.path_params["slug"]
        self.active_connections.append(websocket)
        room: Union[Room, None] = self.groups.get(code_slug)
        if room is None:
            room = Room()
            room.set_user(websocket)
            self.groups[code_slug] = room
        else:
            room.set_user(websocket)
        return room

    async def disconnect(self, websocket: CustomWebSocket) -> None:
        slug = websocket.path_params["slug"]
        room: Room = self.groups.get(slug)
        room.change_user(socket=websocket)
        self.active_connections.remove(websocket)

    async def send_personal_message(
        self, message: dict, websocket: CustomWebSocket
    ) -> None:
        await websocket.send_json(message)

    async def broadcast(self, message: dict, slug: str) -> None:
        room: Room = self.groups.get(slug)
        if room is not None:
            await room.broadcast_message(message=message)
