import base64
import binascii
import io
from decimal import Decimal
from logging import getLogger
from pathlib import Path
from uuid import uuid4

import qrcode.image.svg
from PIL import Image, UnidentifiedImageError
from qrcode import (
    ERROR_CORRECT_H,
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    QRCode,
)
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import (
    HorizontalGradiantColorMask,
    ImageColorMask,
    RadialGradiantColorMask,
    SolidFillColorMask,
    SquareGradiantColorMask,
    VerticalGradiantColorMask,
)
from qrcode.image.styles.moduledrawers.pil import (
    CircleModuleDrawer,
    GappedSquareModuleDrawer,
    HorizontalBarsDrawer,
    RoundedModuleDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer,
)

from schemas.qr import (
    ColorMaskConfig,
    EyeDrawerConfig,
    ModuleDrawerConfig,
)

from .exceptions import QRCodeError

logger = getLogger(__name__)


class QRCodeGeneratorService:
    ERROR_CORRECTION_MAP = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }

    TEMP_DIR = Path(__file__).parent.parent / "temp" / "qr" / "generate"

    @classmethod
    def _ensure_temp_dir(cls):
        cls.TEMP_DIR.mkdir(exist_ok=True)

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )

    @staticmethod
    def _get_module_drawer(config: ModuleDrawerConfig | None):
        if not config:
            return SquareModuleDrawer()

        drawer_map = {
            "square": SquareModuleDrawer,
            "gapped_square": GappedSquareModuleDrawer,
            "circle": CircleModuleDrawer,
            "rounded": RoundedModuleDrawer,
            "vertical_bars": VerticalBarsDrawer,
            "horizontal_bars": HorizontalBarsDrawer,
        }

        drawer_class = drawer_map[config.type]
        kwargs = {}

        if config.size_ratio is not None and config.type in ["gapped_square", "circle"]:
            kwargs["size_ratio"] = Decimal(str(config.size_ratio))

        if config.radius_ratio is not None and config.type == "rounded":
            kwargs["radius_ratio"] = config.radius_ratio

        return drawer_class(**kwargs)

    @staticmethod
    def _get_eye_drawer(config: EyeDrawerConfig | None):
        if not config:
            return None

        if config.type == "square":
            return SquareModuleDrawer()
        elif config.type == "circle":
            return CircleModuleDrawer()
        elif config.type == "rounded":
            kwargs = {}
            if config.radius_ratio is not None:
                kwargs["radius_ratio"] = config.radius_ratio
            return RoundedModuleDrawer(**kwargs)

    @classmethod
    def _get_color_mask(cls, config: ColorMaskConfig | None):
        """Create color mask from config"""
        if not config:
            return None

        back_color = (
            cls._hex_to_rgb(config.back_color) if config.back_color else (255, 255, 255)
        )

        if config.type == "solid":
            front_color = (
                cls._hex_to_rgb(config.front_color) if config.front_color else (0, 0, 0)
            )
            return SolidFillColorMask(back_color=back_color, front_color=front_color)

        elif config.type == "radial_gradient":
            center_color = (
                cls._hex_to_rgb(config.center_color)
                if config.center_color
                else (0, 0, 0)
            )
            edge_color = (
                cls._hex_to_rgb(config.edge_color) if config.edge_color else (0, 0, 255)
            )
            return RadialGradiantColorMask(
                back_color=back_color, center_color=center_color, edge_color=edge_color
            )

        elif config.type == "square_gradient":
            center_color = (
                cls._hex_to_rgb(config.center_color)
                if config.center_color
                else (0, 0, 0)
            )
            edge_color = (
                cls._hex_to_rgb(config.edge_color) if config.edge_color else (0, 0, 255)
            )
            return SquareGradiantColorMask(
                back_color=back_color, center_color=center_color, edge_color=edge_color
            )

        elif config.type == "horizontal_gradient":
            left_color = (
                cls._hex_to_rgb(config.left_color) if config.left_color else (0, 0, 0)
            )
            right_color = (
                cls._hex_to_rgb(config.right_color)
                if config.right_color
                else (0, 0, 255)
            )
            return HorizontalGradiantColorMask(
                back_color=back_color, left_color=left_color, right_color=right_color
            )

        elif config.type == "vertical_gradient":
            top_color = (
                cls._hex_to_rgb(config.top_color) if config.top_color else (0, 0, 0)
            )
            bottom_color = (
                cls._hex_to_rgb(config.bottom_color)
                if config.bottom_color
                else (0, 0, 255)
            )
            return VerticalGradiantColorMask(
                back_color=back_color, top_color=top_color, bottom_color=bottom_color
            )

        elif config.type == "image" and config.color_mask_image:
            cls._ensure_temp_dir()

            if back_color == (0, 0, 0):
                raise QRCodeError(
                    code="invalid_color_combination",
                    message="Pure black background (#000000) cannot be used with "
                    "Image Pattern mode. Use a lighter color.",
                    status_code=400,
                )
            try:
                image_bytes = base64.b64decode(
                    config.color_mask_image.split(",")[1]
                    if "," in config.color_mask_image
                    else config.color_mask_image
                )
                image = Image.open(io.BytesIO(image_bytes))
            except (binascii.Error, UnidentifiedImageError) as exc:
                raise QRCodeError(
                    code="invalid_color_mask_image",
                    message="Invalid color_mask_image data",
                    status_code=400,
                ) from exc
            return ImageColorMask(back_color=back_color, color_mask_image=image)

        return None

    @classmethod
    async def generate_qr(
        cls,
        data: str,
        version: int | None,
        box_size: int,
        border: int,
        error_correction: str,
        output_format: str,
        final_size: int | None,
        fill_color: str | None,
        back_color: str | None,
        use_styled_image: bool,
        module_drawer: ModuleDrawerConfig | None,
        eye_drawer: EyeDrawerConfig | None,
        color_mask: ColorMaskConfig | None,
        embedded_image: str | None,
    ) -> dict:
        if not use_styled_image and (module_drawer or eye_drawer or color_mask):
            raise QRCodeError(
                code="styled_image_required",
                message="Styled image options require use_styled_image=True",
                status_code=400,
            )

        if output_format != "png" and final_size is not None:
            raise QRCodeError(
                code="final_size_png_only",
                message="final_size is only supported for PNG output",
                status_code=400,
            )

        logger.info(f"Generating QR code with format: {output_format}")

        qr = QRCode(
            version=version,
            error_correction=cls.ERROR_CORRECTION_MAP[error_correction],
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        if output_format == "ascii":
            f = io.StringIO()
            qr.print_ascii(out=f)
            f.seek(0)
            return {"image": f.read(), "format": "ascii", "size": None}

        if output_format.startswith("svg"):
            if output_format == "svg":
                factory = qrcode.image.svg.SvgImage
            elif output_format == "svg-path":
                factory = qrcode.image.svg.SvgPathImage
            else:
                factory = qrcode.image.svg.SvgFragmentImage

            img = qr.make_image(image_factory=factory)
            svg_string = img.to_string(encoding="unicode")

            return {"image": svg_string, "format": output_format, "size": None}

        make_image_kwargs = {}
        image_path = None

        if use_styled_image:
            logger.info("Using StyledPilImage for advanced styling")
            make_image_kwargs["image_factory"] = StyledPilImage

            if module_drawer:
                make_image_kwargs["module_drawer"] = cls._get_module_drawer(
                    module_drawer
                )

            if eye_drawer:
                eye_drawer_instance = cls._get_eye_drawer(eye_drawer)
                if eye_drawer_instance:
                    make_image_kwargs["eye_drawer"] = eye_drawer_instance

            if color_mask:
                color_mask_instance = cls._get_color_mask(color_mask)
                if color_mask_instance:
                    make_image_kwargs["color_mask"] = color_mask_instance

            if embedded_image:
                cls._ensure_temp_dir()
                try:
                    image_bytes = base64.b64decode(
                        embedded_image.split(",")[1]
                        if "," in embedded_image
                        else embedded_image
                    )
                    image = Image.open(io.BytesIO(image_bytes))
                except (binascii.Error, UnidentifiedImageError) as exc:
                    raise QRCodeError(
                        code="invalid_embedded_image",
                        message="Invalid embedded_image data",
                        status_code=400,
                    ) from exc
                image_path = cls.TEMP_DIR / f"{uuid4()}.png"
                image.save(image_path)
                make_image_kwargs["embeded_image_path"] = str(image_path)

        else:
            if fill_color:
                make_image_kwargs["fill_color"] = cls._hex_to_rgb(fill_color)
            if back_color:
                make_image_kwargs["back_color"] = cls._hex_to_rgb(back_color)

        img = qr.make_image(**make_image_kwargs)

        if hasattr(img, "convert"):
            img = img.convert("RGB")  # type: ignore

        if final_size and hasattr(img, "resize"):
            img = img.resize(  # type: ignore
                (final_size, final_size), resample=Image.Resampling.LANCZOS
            )

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")  # type: ignore
        qr_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

        size_info = (
            {"width": img.size[0], "height": img.size[1]}  # type: ignore
            if hasattr(img, "size")
            else None
        )

        if image_path:
            image_path.unlink()

        return {"image": qr_data, "format": "png", "size": size_info}
