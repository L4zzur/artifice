from fastapi import APIRouter

from .password import router as password_router

api_router = APIRouter(prefix="", tags=["Password Operations"])

api_router.include_router(password_router)
