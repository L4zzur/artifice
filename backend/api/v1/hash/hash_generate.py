from logging import getLogger

from fastapi import APIRouter, HTTPException

from schemas.error import ErrorResponse
from schemas.hash import (
    HashGenerateRequest,
    HashGenerateResponse,
)
from services.exceptions import ServiceError
from services.hash_service import HashService

router = APIRouter(prefix="/generate")

logger = getLogger(__name__)


@router.post(
    "",
    response_model=HashGenerateResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
async def generate_hash(request: HashGenerateRequest):
    """
    Generate cryptographic hash

    ## Supported Algorithms:
    - **MD5**: 128-bit (legacy, use for checksums only)
    - **SHA-1**: 160-bit (deprecated for security)
    - **SHA-256**: 256-bit (recommended)
    - **SHA-512**: 512-bit (high security)
    - **SHA3-256/512**: SHA-3 family
    - **BLAKE2b/s**: Fast and secure

    ## HMAC Support:
    Provide `hmac_key` for keyed-hash message authentication

    ## Example Request:
    ```
    {
        "data": "Hello, World!",
        "algorithm": "sha256",
        "output_format": "hex"
    }
    ```

    ## Example Response:
    ```
    {
        "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "algorithm": "sha256",
        "format": "hex"
    }
    ```
    """
    try:
        result = HashService.generate_hash(
            data=request.data,
            algorithm=request.algorithm,
            output_format=request.output_format,
            hmac_key=request.hmac_key,
        )

        return HashGenerateResponse(**result)

    except ServiceError as e:
        logger.warning("Hash generation error: %s", e.message)
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "code": e.code,
                "message": e.message,
                "context": e.context,
            },
        )

    except Exception:
        logger.exception("Unexpected error during hash generation")
        raise HTTPException(
            status_code=500,
            detail="Internal hash generation error",
        )
