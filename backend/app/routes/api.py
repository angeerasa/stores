from fastapi import APIRouter, Request
from app.routes import users

api_router = APIRouter()
api_router.include_router(users.router)
