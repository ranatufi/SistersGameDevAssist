import pygame
from pathlib import Path
from game.paths import asset_path
from game.paths import ADV_RIRI_DIR

class ImageManager:
    def __init__(self):
        self.images: dict[tuple[str, tuple[int, int] | None], pygame.Surface] = {}
        #region ゲーム開始前の素材はここで読み込む
        self.image("riri mini.png", ADV_RIRI_DIR, size=(32, 32))
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