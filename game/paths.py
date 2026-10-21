import sys
from pathlib import Path

def resource_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[1]

ASSET_DIR = resource_root() / "assets"

IMAGES_DIR = ASSET_DIR / "images"
SOUNDS_DIR = ASSET_DIR / "sounds"

ADV_DIR = IMAGES_DIR / "adv"
CHARAS_DIR = IMAGES_DIR / "charas"
ITEMS_DIR = IMAGES_DIR / "items"
MAPS_DIR = IMAGES_DIR / "maps"

ADV_BACKGROUND_DIR = ADV_DIR / "backgrounds"
ADV_RIRI_DIR = ADV_DIR / "riri"
ADV_SHO_DIR = ADV_DIR / "sho"

CHARAS_RIRI_DIR = CHARAS_DIR / "riri"

def asset_path(dir: Path, filename: str) -> Path:
    return dir / filename