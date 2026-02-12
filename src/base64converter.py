import base64
import os


async def base64converter(image_file: str) -> str:
    if not os.path.exists(image_file):
        raise FileNotFoundError(f"File not found: {image_file}")

    with open(image_file, "rb") as file:
        image_buffer = file.read()

    return f"data:image/jpeg;base64,{base64.b64encode(image_buffer).decode('utf-8')}"
