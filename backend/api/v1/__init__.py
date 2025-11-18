from fastapi import APIRouter

from .qr_generator import router as qr_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(qr_router)
