from logging import getLogger

from fastapi import APIRouter, HTTPException

from schemas.error import ErrorResponse
from schemas.hash import (
    HashFileRequest,
    HashFileResponse,
)
from services.exceptions import ServiceError
from services.hash_service import HashService

router = APIRouter(prefix="/file")

logger = getLogger(__name__)


@router.post(
    "",
    response_model=HashFileResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
async def hash_file(request: HashFileRequest):
    """
    Calculate cryptographic hash of a file

    ## Use Cases:
    - **File Integrity**: Verify file hasn't been modified
    - **Duplicate Detection**: Compare files by hash
    - **Checksums**: Validate downloads

    ## File Size Limits:
    - Maximum ~50MB (base64 encoded string size limits)
    - For larger files, use streaming or chunked uploads

    ## Example Request:
    ```
    {
        "file_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUh...",
        "algorithm": "sha256",
        "output_format": "hex"
    }
    ```

    ## Example Response:
    ```
    {
        "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "algorithm": "sha256",
        "format": "hex",
        "file_size": 2048
    }
    ```
    """
    try:
        result = HashService.hash_file(
            file_base64=request.file_base64,
            algorithm=request.algorithm,
            output_format=request.output_format,
        )

        return HashFileResponse(**result)

    except ServiceError as e:
        logger.warning("File hash error: %s", e.message)
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "code": e.code,
                "message": e.message,
                "context": e.context,
            },
        )

    except Exception:
        logger.exception("Unexpected error during file hashing")
        raise HTTPException(
            status_code=500,
            detail="Internal file hashing error",
        )
