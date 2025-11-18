from fastapi import APIRouter

from .qr import api_router as qr_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(qr_router)
