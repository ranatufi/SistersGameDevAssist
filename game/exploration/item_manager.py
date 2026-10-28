
import random

import pygame

from game.paths import (
    EXPLORATION_ITEM_DIR,
    EXPLORATION_ITEM_IMAGE,
)


class ItemManager:
    """複数マップにまたがるアイテムを管理する。"""

    def __init__(self, game, item_count=5, item_size=24):
        self.game = game
        self.item_count = item_count
        self.item_size = item_size

        # {"map_name": str, "rect": pygame.Rect} のリスト
        self.items = []
        self.collected_count = 0
        self.game_cleared = False
        self.item_image = None
        self.initialized = False

    def load_image(self):
        """ImageManager経由で画像を読み込む。"""
        self.item_image = self.game.image_manager.image(
            EXPLORATION_ITEM_IMAGE,
            EXPLORATION_ITEM_DIR,
            (self.item_size, self.item_size),
        )

        if self.item_image is None:
            raise FileNotFoundError(
                f"アイテム画像を読み込めません: {EXPLORATION_ITEM_IMAGE}"
            )

    def spawn_items(
        self,
        collision_maps,
        current_map_name,
        player_rect,
    ):
        """
        全マップの歩行可能領域にアイテムを配置する。

        collision_maps:
            {マップ名: CollisionMap} の辞書
        """
        if self.initialized:
            return

        self.items = []

        map_names = list(collision_maps.keys())
        if not map_names:
            raise ValueError("アイテムを配置できるマップがありません")

        # 各マップにできるだけ均等に割り振る
        destinations = [
            map_names[i % len(map_names)]
            for i in range(self.item_count)
        ]
        random.shuffle(destinations)

        for preferred_map in destinations:
            # 希望先に配置できなければ、別のマップを試す
            candidates = [preferred_map] + [
                name for name in map_names
                if name != preferred_map
            ]
            random.shuffle(candidates)
            candidates.remove(preferred_map)
            candidates.insert(0, preferred_map)

            placed = False

            for map_name in candidates:
                collision_map = collision_maps[map_name]

                max_x = collision_map.width - self.item_size
                max_y = collision_map.height - self.item_size

                if max_x < 0 or max_y < 0:
                    continue

                for _ in range(3000):
                    x = random.randint(0, max_x)
                    y = random.randint(0, max_y)

                    rect = pygame.Rect(
                        x, y, self.item_size, self.item_size
                    )

                    if not collision_map.is_rect_walkable(rect):
                        continue

                    # 現在のマップではプレイヤーと重ねない
                    if (
                        map_name == current_map_name
                        and rect.colliderect(player_rect)
                    ):
                        continue

                    # 同じマップのアイテム同士を重ねない
                    if any(
                        item["map_name"] == map_name
                        and item["rect"].colliderect(rect)
                        for item in self.items
                    ):
                        continue

                    self.items.append({
                        "map_name": map_name,
                        "rect": rect,
                    })
                    placed = True
                    break

                if placed:
                    break

            if not placed:
                self.items.clear()
                raise RuntimeError(
                    "アイテムを配置できませんでした。"
                    "各マップの歩行可能領域を確認してください。"
                )

        self.initialized = True

        print(f"アイテム配置数: {len(self.items)}/{self.item_count}")
        for item in self.items:
            rect = item["rect"]
            print(
                f"  マップ={item['map_name']}, "
                f"x={rect.x}, y={rect.y}"
            )

    def collect_items(self, player_rect, current_map_name):
        """現在のマップにあるアイテムを回収する。"""
        if self.game_cleared:
            return

        remaining_items = []

        for item in self.items:
            if item["map_name"] != current_map_name:
                remaining_items.append(item)
                continue

            if player_rect.colliderect(item["rect"]):
                self.collected_count += 1
                print(
                    f"アイテム回収: "
                    f"{self.collected_count}/{self.item_count}"
                )
            else:
                remaining_items.append(item)

        self.items = remaining_items

        if self.collected_count >= self.item_count:
            self.game_cleared = True
            print("ゲームクリア！")

    def draw_items(
        self,
        screen,
        current_map_name,
        offset_x,
        offset_y,
    ):
        """現在のマップに配置されたアイテムを描画する。"""
        if self.item_image is None:
            return

        for item in self.items:
            if item["map_name"] != current_map_name:
                continue

            rect = item["rect"]
            screen.blit(
                self.item_image,
                (rect.x + offset_x, rect.y + offset_y),
            )

    def reset(self):
        """アイテムの回収状況と配置を初期化する。"""
        self.items.clear()
        self.collected_count = 0
        self.game_cleared = False
        self.initialized = False