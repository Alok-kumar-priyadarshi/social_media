import json
import asyncio
from app.core.redis import redis_client
from app.websocket.manager import manager

print("🔥 Redis listener started")

def start_redis_listener(loop):
    pubsub = redis_client.pubsub()
    pubsub.subscribe("chat_channel")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        data = json.loads(message["data"])

        to_user_id = data["to_user_id"]
        text = data["message"]

        asyncio.run_coroutine_threadsafe(
            manager.send_message(to_user_id, text),
            loop
        )

        print("📥 Received from Redis:", data)