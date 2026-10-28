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

ADV_BACKGROUND_DIR = ADV_DIR / "background"
ADV_RIRI_DIR = ADV_DIR / "riri"
ADV_SHO_DIR = ADV_DIR / "sho"

CHARAS_RIRI_DIR = CHARAS_DIR / "riri"
CHARAS_TEKI_DIR = CHARAS_DIR / "teki"

EXPLORATION_BACKGROUND_DIR = MAPS_DIR
EXPLORATION_MAP_DIR = MAPS_DIR
EXPLORATION_CHARACTER_DIR = CHARAS_RIRI_DIR

EXPLORATION_ITEM_DIR = ITEMS_DIR
EXPLORATION_ITEM_IMAGE = "paper.PNG"

EXPLORATION_ENEMY_DIR = CHARAS_TEKI_DIR