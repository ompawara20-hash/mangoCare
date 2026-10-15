"""
Image Processing Utilities: Safe Decoding, EXIF Orientation, and Resizing
"""
import io
from typing import Tuple, Optional
from PIL import Image, ImageOps

class ImageProcessingError(Exception):
    def __init__(self, message: str, error_code: str = "IMAGE_DECODE_FAILED", suggestion: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.suggestion = suggestion or "Please ensure the photograph is not corrupted and can be viewed normally."


# Max pixels safety setting to prevent decompression bomb exploits
Image.MAX_IMAGE_PIXELS = 40_000_000
MIN_DIMENSION = 100
MAX_DIMENSION = 6000


def decode_and_normalize_image(image_bytes: bytes) -> Tuple[Image.Image, int, int]:
    """
    Decodes raw image bytes into a sanitized PIL RGB Image:
    - Verifies decodability
    - Transposes according to EXIF orientation
    - Converts RGBA, grayscale, or palette to pure 3-channel RGB
    - Validates minimum and maximum pixel bounds
    """
    try:
        raw_img = Image.open(io.BytesIO(image_bytes))
        raw_img.verify()
    except Exception as e:
        raise ImageProcessingError(
            f"Unable to parse image data: {str(e)}",
            error_code="CORRUPTED_IMAGE",
            suggestion="The image file appears corrupted. Please re-take or re-export the photo."
        )

    # Re-open stream since verify() closes or invalidates the PIL reader
    try:
        img = Image.open(io.BytesIO(image_bytes))

        # EXIF Orientation correction
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass  # Fallback to untransposed if EXIF is malformed

        width, height = img.size

        if width < MIN_DIMENSION or height < MIN_DIMENSION:
            raise ImageProcessingError(
                f"Image resolution {width}x{height} is too small. Minimum required is {MIN_DIMENSION}x{MIN_DIMENSION}px.",
                error_code="IMAGE_TOO_SMALL",
                suggestion="Please provide a higher-resolution photograph for accurate symptom analysis."
            )

        if width > MAX_DIMENSION or height > MAX_DIMENSION:
            raise ImageProcessingError(
                f"Image resolution {width}x{height} exceeds maximum allowable dimension of {MAX_DIMENSION}px.",
                error_code="IMAGE_TOO_LARGE",
                suggestion="Please downscale the image slightly before uploading."
            )

        # Convert to 3-channel RGB
        if img.mode != "RGB":
            img = img.convert("RGB")

        return img, width, height

    except ImageProcessingError:
        raise
    except Exception as e:
        raise ImageProcessingError(
            f"Error processing image stream: {str(e)}",
            error_code="IMAGE_PROCESSING_EXCEPTION"
        )


def create_safe_thumbnail_bytes(image: Image.Image, max_dim: int = 500) -> bytes:
    """Creates a compact JPEG thumbnail byte buffer for embedding in PDF reports."""
    thumb = image.copy()
    thumb.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    thumb.save(buf, format="JPEG", quality=85)
    return buf.getvalue()
