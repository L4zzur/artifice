from fastapi import APIRouter

from .password import api_router as pass_router
from .qr import api_router as qr_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(qr_router)
api_router.include_router(pass_router)
