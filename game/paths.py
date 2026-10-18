import sys
from pathlib import Path

def resource_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[1]

ASSET_DIR = resource_root() / "assets"

def asset_path(filename: str) -> Path:
    return ASSET_DIR / filename