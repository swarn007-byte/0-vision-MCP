from mcp.server.fastmcp import FastMCP

from open_router import analyze_image
from screen import capture_screen


server = FastMCP("vision-mcp")


@server.tool(name="NoEyeVision", description="give detailed analysis of image")

async def analyser(prompt: str, image_file: str) -> str:
    return await analyze_image(prompt, image_file)


@server.tool(name="screen", description="capture the current screen and return the image path")
def screen(action: str = "capture", target: str | None = None, pid: int | None = None) -> str:
    if action != "capture":
        raise ValueError(f"Unknown screen action: {action}")

    return capture_screen(target=target, pid=pid)


def main() -> None:
    server.run()


if __name__ == "__main__":
    main()
