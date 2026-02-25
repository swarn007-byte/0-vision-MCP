import base64
import os
from pathlib import Path


async def base64converter(image: str) -> str:
    try:
        if not os.path.exists(image):
            raise FileNotFoundError(f"File not found: {image}")

        image_size = Path(image).stat().st_size
        max_size = 30 * 1024 * 1024

        if image_size > max_size:
            raise ValueError(f"{image} exceeds 30 MB limit")

        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".bmp": "image/bmp",
        }

        ext = Path(image).suffix.lower()
        mime = mime_types.get(ext)

        if not mime:
            raise ValueError(f"{ext} extension is not supported")

        with open(image, "rb") as img:
            image_buffer = img.read()

        return f"data:{mime};base64,{base64.b64encode(image_buffer).decode('utf-8')}"

    except Exception as error:
        raise RuntimeError(f"Failed to convert image to base64: {error}") from error