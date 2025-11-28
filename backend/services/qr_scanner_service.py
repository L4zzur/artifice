import base64
import io
from logging import getLogger
from pathlib import Path

import qrlyzer
from PIL import Image, UnidentifiedImageError

from .exceptions import ServiceError

logger = getLogger(__name__)


class QRCodeScannerService:

    TEMP_DIR = Path(__file__).parent.parent / "temp" / "qr" / "scan"

    @classmethod
    def _ensure_temp_dir(cls):
        cls.TEMP_DIR.mkdir(exist_ok=True)

    @classmethod
    async def scan_qr(cls, image_base64: str, auto_resize: bool = True) -> dict:
        """
        Scan QR code(s) from base64 encoded image using qrlyzer

        Args:
            image_base64: Base64 encoded image data
            auto_resize: Enable auto-resizing for better detection (100px-1280px)

        Returns:
            dict with decoded QR codes and metadata

        Raises:
            ServiceError: If image is invalid or no QR codes found
        """
        try:
            image_bytes = base64.b64decode(
                image_base64.split(",")[1] if "," in image_base64 else image_base64
            )
            image = Image.open(io.BytesIO(image_bytes))
        except UnidentifiedImageError as exc:
            raise ServiceError(
                code="invalid_image",
                message="Invalid image data provided",
                status_code=400,
            ) from exc

        try:
            image_gray = image.convert("L")
        except Exception as exc:
            raise ServiceError(
                code="image_processing_failed",
                message="Failed to process image",
                status_code=400,
            ) from exc

        try:
            codes = qrlyzer.detect_and_decode_from_bytes(
                image_gray.tobytes(),
                width=image_gray.width,
                height=image_gray.height,
                auto_resize=auto_resize,
            )

            if not codes or len(codes) == 0:
                raise ServiceError(
                    code="no_qr_code_found",
                    message="No QR codes found in image",
                    status_code=404,
                )

            logger.info(f"Successfully decoded {len(codes)} QR code(s)")

            return {
                "codes": codes,
                "count": len(codes),
                "success": True,
            }

        except ServiceError:
            raise
        except Exception as exc:
            logger.exception("Error during QR code detection/decoding with qrlyzer")
            raise ServiceError(
                code="scan_failed",
                message="Failed to scan QR code from image",
                status_code=500,
                context={"error": str(exc)},
            ) from exc
