import json
import os
import urllib.error
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


def _get_required_env(name: str) -> str:
    value = os.environ.get(name)

    if not value:
        raise ValueError(f"Missing required environment variable: {name}")

    return value


_load_env()


def _read_openrouter_error(error: urllib.error.HTTPError) -> str:
    try:
        return error.read().decode("utf-8")
    except Exception:
        return "no response body"


def _extract_content(data: dict) -> str:
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("OpenRouter returned an unexpected response") from error

    if not content:
        raise RuntimeError("OpenRouter returned an empty response")

    return content


async def analyze_image(prompt: str, image: str) -> str:
    api_key = _get_required_env("OPENROUTER_API_KEY")
    model = _get_required_env("OPENROUTER_MODEL")

    if image.startswith(("http://", "https://")):
        image_encoded = image
    else:
        image_encoded = await base64converter(image)

    body = json.dumps(
        {
            "model": model,
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
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = _read_openrouter_error(error)
        raise RuntimeError(f"OpenRouter request failed with status {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"OpenRouter request failed: {error.reason}") from error
    except TimeoutError as error:
        raise RuntimeError("OpenRouter request timed out after 60 seconds") from error
    except json.JSONDecodeError as error:
        raise RuntimeError("OpenRouter returned invalid JSON") from error

    return _extract_content(data)
