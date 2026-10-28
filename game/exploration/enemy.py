
import math
from pathlib import Path

import pygame

from game.paths import EXPLORATION_ENEMY_DIR


class Enemy:
    SIZE = (48, 64)
    SPEED = 100

    def __init__(self, game, collision_map, position):
        self.game = game
        self.collision_map = collision_map

        self.rect = pygame.Rect(
            position[0],
            position[1],
            *self.SIZE,
        )

        self.direction = "down"
        self.animations = {}

        self.animation_index = 0
        self.animation_timer = 0.0
        self.animation_interval = 0.15

        self.load_animations()
        self.image = self.animations["down"][0]

    def load_animations(self):
        """上下左右の歩行画像を読み込む。"""
        for direction in ("up", "down", "left", "right"):
            folder = Path(EXPLORATION_ENEMY_DIR) / direction

            image_paths = sorted(
                folder.glob("*.png"),
                key=lambda path: (
                    (0, int(path.stem))
                    if path.stem.isdigit()
                    else (1, path.stem)
                ),
            )

            if not image_paths:
                raise FileNotFoundError(
                    f"敵の歩行画像が見つかりません: {folder}"
                )

            self.animations[direction] = [
                self.game.image_manager.image(
                    path.name,
                    folder,
                    self.SIZE,
                )
                for path in image_paths
            ]

    def update(self, dt, player_rect):
        """プレイヤーに向かって8方向に移動する。"""
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery

        distance = math.hypot(dx, dy)

        if distance < 1:
            return

        # 移動方向を正規化する
        dx /= distance
        dy /= distance

        # 画像は4方向なので、移動量の大きい軸で向きを決める
        if abs(dx) > abs(dy):
            new_direction = "right" if dx > 0 else "left"
        else:
            new_direction = "down" if dy > 0 else "up"

        if new_direction != self.direction:
            self.direction = new_direction
            self.animation_index = 0
            self.animation_timer = 0.0

        # 移動距離を計算する
        move_x = round(dx * self.SPEED * dt)
        move_y = round(dy * self.SPEED * dt)

        # 横方向の当たり判定
        if move_x != 0:
            candidate = self.rect.copy()
            candidate.x += move_x

            if self.collision_map.is_rect_walkable(candidate):
                self.rect.x = candidate.x

        # 縦方向の当たり判定
        if move_y != 0:
            candidate = self.rect.copy()
            candidate.y += move_y

            if self.collision_map.is_rect_walkable(candidate):
                self.rect.y = candidate.y

        # 歩行アニメーション
        images = self.animations[self.direction]
        self.animation_timer += dt

        while self.animation_timer >= self.animation_interval:
            self.animation_timer -= self.animation_interval
            self.animation_index = (
                self.animation_index + 1
            ) % len(images)

        self.image = images[self.animation_index]

    def draw(self, screen, offset_x, offset_y):
        """敵を画面に描画する。"""
        screen.blit(
            self.image,
            (
                self.rect.x + offset_x,
                self.rect.y + offset_y,
            ),
        )
