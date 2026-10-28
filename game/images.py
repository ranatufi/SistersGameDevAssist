import pygame
from pathlib import Path
from game.paths import asset_path

class ImageManager:
    def __init__(self):
        self.images: dict[tuple[str, str], pygame.Surface | None,] = {}
        self.scaled_images: dict[tuple[tuple[str, str], tuple[int, int]], pygame.Surface | None, ] = {}
    
    def image(self, filename: str, path: Path, size: tuple[int, int] | None = None) -> pygame.Surface | None:
        image_key = (str(path), filename)
        if image_key not in self.images:
            target_path = asset_path(path, filename)
            try:
                loaded_image = pygame.image.load(str(target_path)).convert_alpha()
            except(pygame.error, OSError) as e:
                print(f"画像の読み込みに失敗: {target_path}, 原因: {e}")
                loaded_image = None
            self.images[image_key] = loaded_image
        original = self.images[image_key]
        if original is None or size is None:
            return original
        if original.get_size() == size:
            return original
        scaled_key = (image_key, size)
        if scaled_key not in self.scaled_images:
            try:
                self.scaled_images[scaled_key] = pygame.transform.smoothscale(original, size)
            except pygame.error as e:
                print(f"画像のスケーリングに失敗: {filename}, 原因: {e}")
                self.scaled_images[scaled_key] = None
        return self.scaled_images[scaled_key]