import json
import platform
import struct
import subprocess
import tempfile
import time
from pathlib import Path


def _png_size(image: str) -> tuple[int | None, int | None]:
    with open(image, "rb") as img:
        header = img.read(24)

    if len(header) >= 24 and header[:8] == b"\x89PNG\r\n\x1a\n":
        width, height = struct.unpack(">II", header[16:24])
        return width, height

    return None, None


def _output_path() -> str:
    directory = Path(tempfile.gettempdir()) / "vision-mcp-captures"
    directory.mkdir(parents=True, exist_ok=True)
    return str(directory / f"capture_{int(time.time() * 1000)}.png")


def _capture_macos(output: str, target: str | None, pid: int | None) -> None:
    if target or pid is not None:
        raise RuntimeError("Window capture by target or pid is not supported on macOS yet")

    subprocess.run(["screencapture", "-x", output], check=True)


def _capture_windows(output: str, target: str | None, pid: int | None) -> None:
    if target or pid is not None:
        raise RuntimeError("Window capture by target or pid is not supported on Windows yet")

    script = f"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
$bitmap.Save("{output}", [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
"""
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        check=True,
    )


def _capture_linux(output: str, target: str | None, pid: int | None) -> None:
    if target or pid is not None:
        raise RuntimeError("Window capture by target or pid is not supported on Linux yet")

    commands = [
        ["gnome-screenshot", "-f", output],
        ["scrot", output],
        ["import", "-window", "root", output],
    ]

    for command in commands:
        try:
            subprocess.run(command, check=True)
            return
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue

    raise RuntimeError("No supported screenshot command found")


def capture_screen(target: str | None = None, pid: int | None = None) -> str:
    output = _output_path()
    system = platform.system()

    try:
        if system == "Darwin":
            _capture_macos(output, target, pid)
        elif system == "Windows":
            _capture_windows(output, target, pid)
        elif system == "Linux":
            _capture_linux(output, target, pid)
        else:
            raise RuntimeError(f"Screen capture is not supported on {system}")
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"Screen capture failed on {system}. Check screen recording permissions."
        ) from error

    width, height = _png_size(output)
    return json.dumps({"image": output, "width": width, "height": height})
