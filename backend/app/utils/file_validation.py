"""
File Upload Validation: Size, MIME type, Extension, and Magic Bytes
"""
from typing import Tuple, Optional
from app.config import settings

class FileValidationError(Exception):
    def __init__(self, message: str, error_code: str = "INVALID_FILE", suggestion: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.suggestion = suggestion or "Please upload a valid JPEG, PNG, or WebP image under 10MB."


# Signatures for common image formats
MAGIC_SIGNATURES = {
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG\r\n\x1a\n": "image/png",
    b"RIFF": "image/webp"  # WEBP has 'RIFF....WEBP'
}


def validate_upload_file(filename: Optional[str], content_type: Optional[str], data: bytes) -> Tuple[str, str]:
    """
    Validates uploaded file payload against security constraints:
    - Non-empty payload
    - File size <= MAX_UPLOAD_SIZE_MB
    - Allowed extension
    - Declared MIME type
    - Binary header signature (magic bytes)
    """
    if not data or len(data) == 0:
        raise FileValidationError(
            "Uploaded file is empty.",
            error_code="EMPTY_FILE",
            suggestion="Select an image file with content and try again."
        )

    if len(data) > settings.MAX_UPLOAD_BYTES:
        raise FileValidationError(
            f"File size exceeds maximum allowable limit of {settings.MAX_UPLOAD_SIZE_MB} MB.",
            error_code="FILE_TOO_LARGE",
            suggestion=f"Please compress or crop the photograph to under {settings.MAX_UPLOAD_SIZE_MB} MB."
        )

    if not filename or "." not in filename:
        raise FileValidationError(
            "Missing or invalid filename.",
            error_code="INVALID_FILENAME",
            suggestion="Ensure the file has a standard extension (.jpg, .png, or .webp)."
        )

    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        allowed_str = ", ".join(settings.ALLOWED_EXTENSIONS).upper()
        raise FileValidationError(
            f"Unsupported file extension '{ext}'. Only {allowed_str} are supported.",
            error_code="UNSUPPORTED_EXTENSION",
            suggestion=f"Please upload an image formatted as {allowed_str}."
        )

    # Magic bytes check
    is_valid_magic = False
    detected_mime = "application/octet-stream"

    if data.startswith(b"\xff\xd8\xff"):
        is_valid_magic = True
        detected_mime = "image/jpeg"
    elif data.startswith(b"\x89PNG\r\n\x1a\n"):
        is_valid_magic = True
        detected_mime = "image/png"
    elif data.startswith(b"RIFF") and len(data) > 12 and data[8:12] == b"WEBP":
        is_valid_magic = True
        detected_mime = "image/webp"

    if not is_valid_magic:
        raise FileValidationError(
            "File header signature does not match a valid JPEG, PNG, or WebP image.",
            error_code="CORRUPTED_FILE_HEADER",
            suggestion="The file may be corrupted or disguised with an incorrect extension. Please export a fresh image."
        )

    return ext, detected_mime
