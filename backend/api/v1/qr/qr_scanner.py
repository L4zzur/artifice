from logging import getLogger

from fastapi import APIRouter, HTTPException

from schemas.error import ErrorResponse
from schemas.qr_scanner import QRScanRequest, QRScanResponse
from services.exceptions import QRCodeError
from services.qr_scanner_service import QRCodeScannerService

router = APIRouter(prefix="/scan")

logger = getLogger(__name__)


@router.post(
    "",
    response_model=QRScanResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "No QR Code Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
async def scan_qr_code(request: QRScanRequest):
    """
    Scan and decode QR code(s) from an image using qrlyzer

    ## Features:
    - **Lightning Fast**: Rust-based QR detection (rqrr + rxing)
    - **Multiple QR Codes**: Detects and decodes multiple QR codes in one image
    - **Auto-Resize**: Automatically scales images (100px-1280px) for optimal detection
    - **High Accuracy**: Works with various QR code sizes and qualities
    - **Lightweight**: Minimal dependencies, perfect for small VPS deployments
    - **Multiple Formats**: Supports PNG, JPG, WEBP, and other common formats

    ## Auto-Resize Feature:

    When enabled (default), the image is automatically resized in 5 steps from 100px
    to 1280px in the largest direction.
    This improves both accuracy and speed, especially for:
    - Large images with small QR codes
    - High-resolution photos
    - Images with multiple QR codes at different scales

    ## Example Request:

    ```
    {
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA...",
        "auto_resize": true
    }
    ```

    ## Example Response:

    ```
    {
        "codes": [
            "https://example.com",
            "Hello, World!"
        ],
        "count": 2,
        "success": true
    }
    ```
    """

    try:
        result = await QRCodeScannerService.scan_qr(
            image_base64=request.image, auto_resize=request.auto_resize
        )

        return QRScanResponse(
            codes=result["codes"],
            count=result["count"],
            success=result["success"],
        )

    except QRCodeError as e:
        logger.warning("QRCodeError: %s", e.message)
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "code": e.code,
                "message": e.message,
                "context": e.context,
            },
        )

    except Exception:
        logger.exception("Unexpected error scanning QR code")
        raise HTTPException(
            status_code=500,
            detail="Internal QR code scanning error",
        )
