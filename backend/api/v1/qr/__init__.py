from fastapi import APIRouter

from .qr_generator import router as generator_router

api_router = APIRouter(prefix="/qr", tags=["QR Code Operations"])

api_router.include_router(generator_router)
