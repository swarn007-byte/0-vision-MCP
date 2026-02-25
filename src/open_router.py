import json
import os
import sys
import urllib.request

from base64converter import base64converter


def _load_env() -> None:
    if not os.path.exists(".env"):
        return

    with open(".env", "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env()

async def analyze_image(prompt: str, image: str) -> str:
    if image.startswith(("http://", "https://")):
        image_encoded = image
    else:
        image_encoded = await base64converter(image)

    body = json.dumps(
        {
            "model": os.environ.get("OPENROUTER_MODEL"),
            "max_tokens": 500,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_encoded}},
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))

    print(json.dumps(data, indent=2), file=sys.stderr)
    return data["choices"][0]["message"]["content"]
