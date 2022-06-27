from fastapi import WebSocket
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.groups = {}

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        w_id = websocket.path_params["id"]
        self.active_connections.append(websocket)
        connection_dict = self.groups.get(w_id)
        if connection_dict is None:
            connection_dict = {}
            if user == ("editor"):
                connection_dict["editor"] = websocket
            else:
                connection_dict["viewers"] = []
                connection_dict["viewers"].append(websocket)
            self.groups[w_id] = connection_dict
        else:
            if user == ("editor"):
                connection_dict["editor"] = websocket
            else:
                if not connection_dict.get("viewers"):
                    connection_dict["viewers"] = []
                connection_dict["viewers"].append(websocket)

    async def disconnect(self, websocket: WebSocket):
        await websocket.close()
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str, id: int):
        viewers_group = self.groups.get(str(id)).get("viewers")
        if viewers_group is not None:
            for viewer in viewers_group:
                await viewer.send_json(message)
