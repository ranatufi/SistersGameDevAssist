import pygame
from pathlib import Path
from game.paths import asset_path

class AssetManager:
    def __init__(self):
        self.images: dict[tuple[str, tuple[int, int] | None], pygame.Surface] = {}
        self.sounds: dict[str, pygame.mixer.Sound | None] = {}

    def image(self, filename: str, size: tuple[int, int] | None = None) -> pygame.Surface | None:
        key = (filename, size)
        if key in self.images:
            return self.images[key]
        path = asset_path(filename)
        try:
            image = pygame.image.load(str(path)).convert_alpha()
            if size:
                image = pygame.transform.smoothscale(image, size)
        except(pygame.error, OSError):
            image = None
        self.images[key] = image
        return image

    def sound(self, filename: str) -> pygame.mixer.Sound | None:
        if filename in self.sounds:
            return self.sounds[filename]
        try:
            sound = pygame.mixer.Sound(str(asset_path(filename)))
        except(pygame.error, OSError):
            sound = None
        self.sounds[filename] = sound
        return sound