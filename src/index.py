from mcp.server.fastmcp import FastMCP

from open_router import analyze_image


server = FastMCP("vision-mcp")


@server.tool(name="NoEyeVision", description="give detailed analysis of image")
async def no_eye_vision(prompt: str, image_file: str) -> str:
    return await analyze_image(prompt, image_file)


def main() -> None:
    server.run()


if __name__ == "__main__":
    main()
