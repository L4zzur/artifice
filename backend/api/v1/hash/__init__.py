from fastapi import APIRouter

from .hash_file import router as file_router
from .hash_generate import router as generate_router
from .hash_info import router as info_router
from .hash_verify import router as verify_router

api_router = APIRouter(prefix="/hash", tags=["Hash Operations"])

api_router.include_router(generate_router)
api_router.include_router(verify_router)
api_router.include_router(info_router)
api_router.include_router(file_router)
