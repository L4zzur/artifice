# schemas/qr_scanner.py
from pydantic import BaseModel, Field


class QRScanRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image containing QR code")
    auto_resize: bool = Field(
        default=True, description="Enable automatic image resizing for better detection"
    )


class QRScanResponse(BaseModel):
    codes: list[str] = Field(
        ..., description="List of decoded QR codes found in the image"
    )
    count: int = Field(..., description="Number of QR codes detected")
    success: bool = Field(..., description="Whether scan was successful")
