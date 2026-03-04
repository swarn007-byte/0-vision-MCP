# 0eye-vision-MCP

Give any text-only LLM the power of vision instantly.

## Prerequisites

- Python 3.10+
- An OpenRouter API key with access to a vision model

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```env
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=google/gemini-2.0-flash-lite:free
```

## MCP Client Config

```json
{
  "mcpServers": {
    "0eye-vision": {
      "command": "python3",
      "args": ["/absolute/path/to/0eye-vision-MCP/src/index.py"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-v1-...",
        "OPENROUTER_MODEL": "google/gemini-2.0-flash-lite:free"
      }
    }
  }
}
```

## Tool

### `NoEyeVision`

Analyze any image using a vision model and get a natural language description.

| Argument | Type | Required | Description |
|---|---|---|---|
| `prompt` | string | yes | What you want to know about the image |
| `image_file` | string | yes | Local image path or http/https image URL |

### `screen`

Capture the current screen and return the saved screenshot path.

| Argument | Type | Required | Description |
|---|---|---|---|
| `action` | string | no | Use `capture` |
| `target` | string | no | Reserved for capturing a specific app/window |
| `pid` | number | no | Reserved for capturing a specific process |

Example response:

```json
{
  "image": "/tmp/vision-mcp-captures/capture_123.png",
  "width": 1440,
  "height": 900
}
```

## Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python3 src/index.py
```

## Project Structure

```text
src/
├── index.py
├── open_router.py
├── base64converter.py
└── screen.py
```
