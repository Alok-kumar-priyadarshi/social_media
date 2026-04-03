# This file is responsible for managing active WebSocket connections
# and sending messages between users

from typing import Dict
from fastapi import WebSocket
from app.core.redis import redis_client
import json
from typing import Dict , List



class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int , List[WebSocket]] = {}

    async def connect(self, user_id:int, websocket:WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
            
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)

            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
            
                
    async def send_message(self, user_id: int, message: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_text(message)
        
            
    def publish_message(self, to_user_id: int, message: str):
        redis_client.publish(
            "chat_channel",
            json.dumps({
                "to_user_id": to_user_id,
                "message": message
            })
        )
            
manager = ConnectionManager()