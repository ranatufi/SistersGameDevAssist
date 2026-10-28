
import math
import random

from game.exploration.enemy import Enemy


class EnemyManager:
    def __init__(
        self,
        game,
        spawn_probability=0.35,
        min_spawn_distance=160,
    ):
        self.game = game
        self.spawn_probability = spawn_probability
        self.min_spawn_distance = min_spawn_distance

        self.enemies = []

    def enter_map(self, collision_map, player_rect):
        """マップに入るたびに敵の出現判定を行う。"""
        # 前のマップの敵を消す
        self.enemies.clear()

        # 出現確率に基づいて抽選する
        if random.random() >= self.spawn_probability:
            print("敵は出現しませんでした")
            return

        position = self.find_spawn_position(
            collision_map,
            player_rect,
        )

        if position is None:
            print("敵を配置できる場所がありません")
            return

        enemy = Enemy(
            self.game,
            collision_map,
            position,
        )

        self.enemies.append(enemy)

        print(
            f"敵が出現しました: "
            f"x={position[0]}, y={position[1]}"
        )

    def find_spawn_position(self, collision_map, player_rect):
        """プレイヤーから離れた歩行可能位置を探す。"""
        enemy_width, enemy_height = Enemy.SIZE

        max_x = collision_map.width - enemy_width
        max_y = collision_map.height - enemy_height

        if max_x < 0 or max_y < 0:
            return None

        for _ in range(2000):
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)

            candidate = player_rect.copy()
            candidate.size = Enemy.SIZE
            candidate.topleft = (x, y)

            if not collision_map.is_rect_walkable(candidate):
                continue

            distance = math.hypot(
                candidate.centerx - player_rect.centerx,
                candidate.centery - player_rect.centery,
            )

            if distance < self.min_spawn_distance:
                continue

            return x, y

        return None

    def update(self, dt, player_rect):
        """現在の敵を更新する。"""
        for enemy in self.enemies:
            enemy.update(dt, player_rect)

    def draw(self, screen, offset_x, offset_y):
        """現在の敵を描画する。"""
        for enemy in self.enemies:
            enemy.draw(screen, offset_x, offset_y)
