from fastapi import APIRouter

from .hash_generate import router as generate_router

api_router = APIRouter(prefix="/hash", tags=["Hash Operations"])

api_router.include_router(generate_router)
