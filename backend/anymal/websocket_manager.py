from typing import List
from fastapi import WebSocket, Depends
from .users import current_active_user
from .db import User
active_connections: List[WebSocket] = []

async def connect(websocket: WebSocket, user:User):
    await websocket.accept()
    active_connections.append(websocket)

def disconnect(websocket: WebSocket):
    active_connections.remove(websocket)

async def broadcast(message: str):
    for connection in active_connections:
        await connection.send_text(message)
