from logging import getLogger

from fastapi import APIRouter, HTTPException

from schemas.error import ErrorResponse
from schemas.hash import (
    HashVerifyRequest,
    HashVerifyResponse,
)
from services.exceptions import ServiceError
from services.hash_service import HashService

router = APIRouter(prefix="/verify")

logger = getLogger(__name__)


@router.post(
    "",
    response_model=HashVerifyResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
async def verify_hash(request: HashVerifyRequest):
    """
    Verify cryptographic hash

    ## Auto-Detection:
    Hash format (hex/base64) is automatically detected if not specified

    ## Example Request:
    ```
    {
        "data": "Hello, World!",
        "expected_hash": "dffd6021bb2bd5b0...",
        "algorithm": "sha256"
    }
    ```

    ## Example Response:
    ```
    {
        "valid": true,
        "algorithm": "sha256"
    }
    ```
    """
    try:
        result = HashService.verify_hash(
            data=request.data,
            expected_hash=request.expected_hash,
            algorithm=request.algorithm,
            output_format=request.output_format,
            hmac_key=request.hmac_key,
        )

        return HashVerifyResponse(**result)

    except ServiceError as e:
        logger.warning("Hash verification error: %s", e.message)
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "code": e.code,
                "message": e.message,
                "context": e.context,
            },
        )

    except Exception:
        logger.exception("Unexpected error during hash verification")
        raise HTTPException(
            status_code=500,
            detail="Internal hash verification error",
        )
