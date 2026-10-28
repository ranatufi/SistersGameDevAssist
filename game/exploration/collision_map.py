import pygame


class CollisionMap:
    WALKABLE_COLOR = (255, 0, 0)

    def __init__(self, image: pygame.Surface):
        self.image = image.convert()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def is_rect_walkable(self, rect: pygame.Rect) -> bool:
        if (
            rect.left < 0
            or rect.top < 0
            or rect.right > self.width
            or rect.bottom > self.height
        ):
            return False

        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                if self.image.get_at((x, y))[:3] != self.WALKABLE_COLOR:
                    return False

        return True