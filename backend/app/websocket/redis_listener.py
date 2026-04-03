# This file listens to Redis pub/sub and forwards messages to users

import json
from app.core.redis import redis_client
from app.websocket.manager import manager

print("🔥 Redis listener started")


def start_redis_listener():
    pubsub = redis_client.pubsub()
    pubsub.subscribe("chat_channel")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        data = json.loads(message["data"])

        to_user_id = data["to_user_id"]
        text = data["message"]

        # Send to connected user (if on this server)
        import asyncio
        asyncio.run(manager.send_message(to_user_id, text))
        
        print("📥 Received from Redis:", data)