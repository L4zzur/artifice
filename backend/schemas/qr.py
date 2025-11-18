from enum import Enum

from pydantic import BaseModel, Field


class ModuleDrawerType(str, Enum):
    square = "square"
    gapped_square = "gapped_square"
    circle = "circle"
    rounded = "rounded"
    vertical_bars = "vertical_bars"
    horizontal_bars = "horizontal_bars"


class EyeDrawerType(str, Enum):
    square = "square"
    rounded = "rounded"
    circle = "circle"


class ColorMaskType(str, Enum):
    solid = "solid"
    radial_gradient = "radial_gradient"
    square_gradient = "square_gradient"
    horizontal_gradient = "horizontal_gradient"
    vertical_gradient = "vertical_gradient"
    image = "image"


class OutputFormat(str, Enum):
    png = "png"
    svg = "svg"
    svg_path = "svg-path"
    svg_fragment = "svg-fragment"
    ascii = "ascii"


class ErrorCorrection(str, Enum):
    L = "L"
    M = "M"
    Q = "Q"
    H = "H"


class ModuleDrawerConfig(BaseModel):
    """Configuration for module drawer styling"""

    type: ModuleDrawerType = Field(
        default=ModuleDrawerType.square, description="Type of module drawer"
    )
    size_ratio: float | None = Field(
        default=None,
        ge=0.1,
        le=1.0,
        description="Size ratio for gapped styles (0.1-1.0)",
    )
    radius_ratio: float | None = Field(
        default=None, description="Radius ratio for rounded corners"
    )


class EyeDrawerConfig(BaseModel):
    """Configuration for eye (position marker) styling"""

    type: EyeDrawerType = Field(
        default=EyeDrawerType.square, description="Type of eye drawer"
    )
    radius_ratio: float | None = Field(
        default=None, description="Radius ratio for rounded eyes"
    )


class ColorMaskConfig(BaseModel):
    """Configuration for color mask"""

    type: ColorMaskType = Field(
        default=ColorMaskType.solid, description="Type of color mask"
    )

    # Solid fill colors
    front_color: str | None = Field(
        default=None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        description="Front/fill color for solid mask",
    )
    back_color: str | None = Field(
        default=None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        description="Background color",
    )

    # Gradient colors
    center_color: str | None = Field(
        default=None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        description="Center color for radial/square gradients",
    )
    edge_color: str | None = Field(
        default=None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        description="Edge color for radial/square gradients",
    )
    left_color: str | None = Field(
        default=None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        description="Left color for horizontal gradient",
    )
    right_color: str | None = Field(
        default=None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        description="Right color for horizontal gradient",
    )
    top_color: str | None = Field(
        default=None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        description="Top color for vertical gradient",
    )
    bottom_color: str | None = Field(
        default=None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        description="Bottom color for vertical gradient",
    )

    # Image color mask
    color_mask_image: str | None = Field(
        default=None, description="Base64 encoded image for image color mask"
    )


class QRCodeRequest(BaseModel):
    data: str = Field(
        ...,
        min_length=1,
        max_length=3000,
        description="The data to be encoded in the QR code",
    )

    # QR code parameters
    version: int | None = Field(
        default=None, ge=1, le=40, description="QR code version (1-40), None for auto"
    )
    box_size: int = Field(
        default=10, ge=1, le=100, description="Size of each box in pixels"
    )
    border: int = Field(
        default=4, ge=0, le=20, description="Border thickness in boxes (min 4 per spec)"
    )
    error_correction: ErrorCorrection = Field(
        default=ErrorCorrection.M,
        description="Error correction level: L(7%), M(15%), Q(25%), H(30%)",
    )

    # Output parameters
    output_format: OutputFormat = Field(
        default=OutputFormat.png, description="Output format"
    )
    final_size: int | None = Field(
        default=None,
        ge=100,
        le=2000,
        description="Final image size (for PNG only, after generation)",
    )

    # Basic styling (for non-styled images)
    fill_color: str | None = Field(
        default=None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        description="Fill color (basic mode only)",
    )
    back_color: str | None = Field(
        default=None,
        pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        description="Background color (basic mode only)",
    )

    # Advanced styling (StyledPilImage)
    use_styled_image: bool = Field(
        default=False, description="Use StyledPilImage for advanced styling"
    )
    module_drawer: ModuleDrawerConfig | None = Field(
        default=None, description="Module drawer configuration for styled images"
    )
    eye_drawer: EyeDrawerConfig | None = Field(
        default=None, description="Eye drawer configuration for styled images"
    )
    color_mask: ColorMaskConfig | None = Field(
        default=None, description="Color mask configuration for styled images"
    )

    # Embedded image
    embedded_image: str | None = Field(
        default=None, description="Base64 encoded image to embed in center"
    )


class QRCodeResponse(BaseModel):
    image: str = Field(description="Base64 encoded image or SVG/ASCII string")
    format: str = Field(description="Output format")
    size: dict | None = Field(
        default=None, description="Image dimensions if applicable"
    )
