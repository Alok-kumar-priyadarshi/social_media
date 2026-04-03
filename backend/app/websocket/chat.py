# This file is responsible for handling WebSocket chat communication
# between users

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from datetime import datetime

from app.websocket.manager import manager

from app.services.message_service import create_message
from app.db.database import SessionLocal

from app.core.security import decode_access_token
import logging

logger = logging.getLogger(__name__)



router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    token = websocket.query_params.get("token")
    
    if not token:
        await websocket.close()
        return 
    
    payload = decode_access_token(token)
    
    if not payload:
        await websocket.close()
        return 
    
    user_id = payload.get("user_id")
    
    await manager.connect(user_id, websocket)
    db = SessionLocal()

    try:
        while True:
            data = await websocket.receive_text()

            message_data = json.loads(data)

            if message_data.get("type") == "typing":
                await manager.publish_message(
                    message_data["to_user_id"],
                    json.dumps({
                        "type": "typing",
                        "sender_id": user_id
                    })
                )
                continue
            if message_data.get("type") == "seen":
                await manager.publish_message(
                    message_data["to_user_id"],
                    json.dumps({
                        "type": "seen",
                        "sender_id": user_id
                    })
                )
                continue
            
            
            
            to_user_id = message_data.get("to_user_id")
            
            message = message_data.get("message")

            if not to_user_id or not message:
                continue
            
            try:
                create_message(db, user_id, to_user_id, message)

                await manager.publish_message(
                    to_user_id,
                    json.dumps({
                        "sender_id": user_id,
                        "message": message,
                        "created_at": str(datetime.utcnow())
                    })
                )

            except Exception as e:
                logger.error(f"Message handling failed: {str(e)}")

    except WebSocketDisconnect:
        manager.disconnect(user_id,websocket)
        db.close()
    
    
    
    
    
    
