import pygame
from pathlib import Path
from game.paths import asset_path
from game.paths import SOUNDS_DIR, ADV_RIRI_DIR

class AssetsManager:
    def __init__(self):
        self.images: dict[tuple[str, tuple[int, int] | None], pygame.Surface] = {}
        self.sounds: dict[str, pygame.mixer.Sound | None] = {}
        #region 素材取り込み
        self.image("riri mini.png", ADV_RIRI_DIR, size=(32, 32))
        self.sound("死神のリスト.mp3", SOUNDS_DIR)
        #endregion

    def image(self, filename: str, path: Path, size: tuple[int, int] | None = None) -> pygame.Surface | None:
        key = (filename, size)
        if key in self.images:
            return self.images[key]
        target_path = asset_path(path, filename)
        try:
            image = pygame.image.load(str(target_path)).convert_alpha()
            if size:
                image = pygame.transform.smoothscale(image, size)
        except(pygame.error, OSError) as e:
            print(f"画像の読み込みに失敗: {target_path}, 原因: {e}")
            image = None
        self.images[key] = image
        return image

    def sound(self, filename: str, path: Path,) -> pygame.mixer.Sound | None:
        if filename in self.sounds:
            return self.sounds[filename]
        try:    
            target_path = asset_path(path, filename)
            sound = pygame.mixer.Sound(str(target_path))
        except(pygame.error, OSError) as e:
            print(f"音声の読み込みに失敗: {target_path}, 原因: {e}")
            sound = None
        self.sounds[filename] = sound
        return sound