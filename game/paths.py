import sys
from pathlib import Path

def resource_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[1]

def asset_path(dir: Path, filename: str) -> Path:
    return dir / filename

ASSET_DIR = resource_root() / "assets"

AUDIOS_DIR = ASSET_DIR / "audios"
IMAGES_DIR = ASSET_DIR / "images"

ADV_DIR = IMAGES_DIR / "adv"
CHARAS_DIR = IMAGES_DIR / "charas"
ITEMS_DIR = IMAGES_DIR / "items"
MAPS_DIR = IMAGES_DIR / "maps"

BGM_DIR = AUDIOS_DIR / "bgm"
SE_DIR = AUDIOS_DIR / "se"

ADV_BACKGROUND_DIR = ADV_DIR / "backgrounds"
ADV_RIRI_DIR = ADV_DIR / "riri"
ADV_SHO_DIR = ADV_DIR / "sho"

CHARAS_RIRI_DIR = CHARAS_DIR / "riri"