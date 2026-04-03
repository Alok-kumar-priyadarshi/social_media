# What this file does:
# - Entry point of the application

# Why it exists:
# - Initializes FastAPI app and registers routes

# How it interacts:
# - Includes API routers

from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.api.routes.user import router as user_router
from app.api.routes.auth import router as auth_router
from app.api.deps import get_current_user
from app.api.routes.follow import router as follow_router
from app.api.routes.block import router as block_router
from app.api.routes.profile import router as profile_router
from app.api.routes.post import router as post_router
from app.api.routes.upload import router as upload_router
from app.api.routes.like import router as like_router
from app.api.routes.message import router as message_router
from app.api.routes.comment import router as comment_router
# from fastapi.staticfiles import StaticFiles

from app.websocket.chat import router as chat_router
import threading
from app.websocket.redis_listener import start_redis_listener

from fastapi.middleware.cors import CORSMiddleware

import os

origins = os.getenv("CORS_ORIGINS")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(follow_router)
app.include_router(block_router)
app.include_router(profile_router)
app.include_router(post_router)
app.include_router(upload_router)
app.include_router(like_router)
app.include_router(message_router)
app.include_router(comment_router)

# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(chat_router)



@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_redis_listener, daemon=True)
    thread.start()

@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {
        "message": "Authenticated user fetched from DB ✅",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }

