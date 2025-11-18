from logging import getLogger

from fastapi import APIRouter, HTTPException

from schemas.error import ErrorResponse
from schemas.qr import QRCodeRequest, QRCodeResponse
from services.exceptions import QRCodeError
from services.qr_generator_service import QRCodeGeneratorService

router = APIRouter(prefix="/qr", tags=["QR Code Operations"])

logger = getLogger(__name__)


@router.post(
    "/generate",
    response_model=QRCodeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
async def generate_qr_code(request: QRCodeRequest):
    """
    Generate QR code with comprehensive styling options

    ## Features:
    - **Basic QR Generation**: Simple black and white QR codes
    - **Custom Colors**: Fill and background colors
    - **Advanced Styling**: Module drawers (circles, rounded, gapped, etc.)
    - **Gradients**: Radial, square, horizontal, vertical gradients
    - **Embedded Images**: Center logos/images
    - **Multiple Formats**: PNG, SVG, ASCII
    - **Error Correction**: L (7%), M (15%), Q (25%), H (30%)
    - **Custom Eyes**: Styled position markers

    ## Examples:

    ### Basic QR Code:
    ```
    {
        "data": "https://example.com",
        "error_correction": "M"
    }
    ```

    ### Styled QR Code with Rounded Corners:
    ```
    {
        "data": "https://example.com",
        "use_styled_image": true,
        "error_correction": "H",
        "module_drawer": {
            "type": "rounded",
            "radius_ratio": 0.8
        },
        "color_mask": {
            "type": "radial_gradient",
            "center_color": "#FF0000",
            "edge_color": "#0000FF"
        }
    }
    ```

    ### QR Code with Embedded Logo:
    ```
    {
        "data": "https://example.com",
        "use_styled_image": true,
        "error_correction": "H",
        "embedded_image": "data:image/png;base64,..."
    }
    ```
    """

    try:
        result = await QRCodeGeneratorService.generate_qr(
            data=request.data,
            version=request.version,
            box_size=request.box_size,
            border=request.border,
            error_correction=request.error_correction,
            output_format=request.output_format,
            final_size=request.final_size,
            fill_color=request.fill_color,
            back_color=request.back_color,
            use_styled_image=request.use_styled_image,
            module_drawer=request.module_drawer,
            eye_drawer=request.eye_drawer,
            color_mask=request.color_mask,
            embedded_image=request.embedded_image,
        )

        return QRCodeResponse(
            image=result["image"], format=result["format"], size=result["size"]
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
        logger.exception("Unexpected error generating QR code")
        raise HTTPException(
            status_code=500,
            detail="Internal QR code generation error",
        )


@router.get("/module-drawers")
async def list_module_drawers():
    return {
        "module_drawers": [
            {"type": "square", "description": "Standard square modules"},
            {
                "type": "gapped_square",
                "description": "Square modules with gaps",
                "supports_size_ratio": True,
            },
            {
                "type": "circle",
                "description": "Circular modules",
                "supports_size_ratio": True,
            },
            {
                "type": "rounded",
                "description": "Rounded corner modules",
                "supports_radius_ratio": True,
            },
            {"type": "vertical_bars", "description": "Vertical bar modules"},
            {"type": "horizontal_bars", "description": "Horizontal bar modules"},
        ]
    }


@router.get("/color-masks")
async def list_color_masks():
    return {
        "color_masks": [
            {
                "type": "solid",
                "description": "Solid fill color",
                "params": ["front_color", "back_color"],
            },
            {
                "type": "radial_gradient",
                "description": "Radial gradient from center",
                "params": ["center_color", "edge_color", "back_color"],
            },
            {
                "type": "square_gradient",
                "description": "Square gradient from center",
                "params": ["center_color", "edge_color", "back_color"],
            },
            {
                "type": "horizontal_gradient",
                "description": "Horizontal gradient",
                "params": ["left_color", "right_color", "back_color"],
            },
            {
                "type": "vertical_gradient",
                "description": "Vertical gradient",
                "params": ["top_color", "bottom_color", "back_color"],
            },
            {
                "type": "image",
                "description": "Image-based coloring",
                "params": ["color_mask_image", "back_color"],
            },
        ]
    }


@router.get("/error-correction-levels")
async def list_error_correction():
    return {
        "levels": [
            {
                "code": "L",
                "recovery": "~7%",
                "description": "Low - About 7% or less errors can be corrected",
            },
            {
                "code": "M",
                "recovery": "~15%",
                "description": (
                    "Medium (default) - About 15%" " or less errors can be corrected"
                ),
            },
            {
                "code": "Q",
                "recovery": "~25%",
                "description": "Quartile - About 25% or less errors can be corrected",
            },
            {
                "code": "H",
                "recovery": "~30%",
                "description": (
                    "High - About 30% or less errors can be corrected "
                    "(recommended for embedded images)"
                ),
            },
        ]
    }
