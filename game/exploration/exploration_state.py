import math
import random
from pathlib import Path

import pygame

from game.states import BaseState
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR
from game.paths import (
    EXPLORATION_BACKGROUND_DIR,
    EXPLORATION_MAP_DIR,
    EXPLORATION_CHARACTER_DIR,
)
from game.exploration.collision_map import CollisionMap
from game.exploration.map_manager import MapManager
from game.exploration.item_manager import ItemManager
from game.exploration.enemy_manager import EnemyManager


class ExplorationState(BaseState):
    # プレイヤー設定（画像サイズ）
    PLAYER_SIZE = (48, 64)
    PLAYER_SPEED = 180

    # 当たり判定のサイズと、画像左上からのオフセット
    # 画像は48x64のまま、当たり判定を足元付近の24x20にする
    PLAYER_COLLISION_SIZE = (24, 20)
    PLAYER_COLLISION_OFFSET = (12, 40)

    # 音声ファイル名
    HEARTBEAT_BGM = "心臓の鼓動.mp3"
    DOOR_OPEN_SE = "ドアを開ける2.mp3"
    DOOR_CLOSE_SE = "door_close.wav"

    # 暗転設定
    FADE_SPEED = 510

    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)

        self.map_manager = MapManager()

        # 画像の描画位置・サイズを管理するRect
        self.player_image_rect = pygame.Rect(
            0, 0,
            self.PLAYER_SIZE[0],
            self.PLAYER_SIZE[1],
        )

        # 壁・敵・アイテム・扉の判定に使う小さなRect
        self.player_rect = pygame.Rect(
            0, 0,
            self.PLAYER_COLLISION_SIZE[0],
            self.PLAYER_COLLISION_SIZE[1],
        )

        self.player_direction = "down"
        self.animation_images = {}
        self.animation_index = 0
        self.animation_timer = 0.0
        self.animation_interval = 0.15
        self.player_image = None

        self.background_image = None
        self.collision_map = None

        self.item_manager = ItemManager(
            game,
            item_count=5,
            item_size=24,
        )

        self.enemy_manager = EnemyManager(game)

        # マップ移動用の領域
        self.map_transitions = [
            {
                "from_map": "room",
                "entrance_id": "room_to_hallwayR",
                "area": pygame.Rect(400, 440, 50, 50),
            },
            {
                "from_map": "room",
                "entrance_id": "room_to_hallwayL",
                "area": pygame.Rect(40, 440, 50, 50),
            },
            {
                "from_map": "hallwayR",
                "entrance_id": "hallwayR_to_room",
                "area": pygame.Rect(0, 300, 50, 50),
            },
            {
                "from_map": "syosai",
                "entrance_id": "syosai_to_hallwayL",
                "area": pygame.Rect(290, 290, 50, 50),
            },
            {
                "from_map": "hallwayL",
                "entrance_id": "hallwayL_to_syosai",
                "area": pygame.Rect(50, 280, 50, 50),
            },
            {
                "from_map": "hallwayL",
                "entrance_id": "hallwayL_to_room",
                "area": pygame.Rect(100, 360, 50, 50),
            },
        ]

        # 暗転・リスタート用
        self.is_dying = False
        self.fade_alpha = 0
        self.fade_direction = 0
        self.reset_done = False

        self.font = pygame.font.SysFont("Yu Gothic", 28, bold=True)
        self.small_font = pygame.font.SysFont("Yu Gothic", 20)

    # --------------------------------------------------
    # ステート開始・終了
    # --------------------------------------------------

    def enter(self):
        """探索画面に入ったときの初期化。"""

        self.load_animation_images()

        # アイテム画像を読み込む。画像未読込だと配置されても表示されない。
        self.item_manager.load_image()

        # 初期マップ
        start_map = self.map_manager.current_map_name
        map_data = self.map_manager.current_map

        self.load_map(
            start_map,
            spawn_position=map_data.start_position,
        )

        # 各マップの当たり判定マップを読み込む
        collision_maps = self.create_collision_maps()

        # アイテムを全マップに配置
        if not self.item_manager.initialized:
            self.item_manager.spawn_items(
                collision_maps,
                self.map_manager.current_map_name,
                self.player_rect,
            )

        # 現在のマップに敵を配置
        self.enemy_manager.enter_map(
            self.collision_map,
            self.player_rect,
        )

        self.sync_heartbeat_bgm()

    def exit(self):
        """探索画面を終了するときの処理。"""
        self.game.audio_manager.stop_bgm()

    # --------------------------------------------------
    # マップ読み込み
    # --------------------------------------------------

    def create_collision_maps(self):
        """すべてのマップの当たり判定データを作成する。"""

        collision_maps = {}

        for map_name, map_data in self.map_manager.maps.items():
            collision_image = self.game.image_manager.image(
                map_data.collision_file,
                EXPLORATION_MAP_DIR,
            )

            if collision_image is None:
                raise FileNotFoundError(
                    f"当たり判定画像を読み込めません: "
                    f"{map_data.collision_file}"
                )

            collision_maps[map_name] = CollisionMap(collision_image)

        return collision_maps

    def load_map(self, map_name, spawn_position=None):
        """指定したマップを読み込む。"""

        map_data = self.map_manager.change_map(map_name)

        self.background_image = self.game.image_manager.image(
            map_data.background_file,
            EXPLORATION_BACKGROUND_DIR,
        )

        collision_image = self.game.image_manager.image(
            map_data.collision_file,
            EXPLORATION_MAP_DIR,
        )

        if self.background_image is None:
            raise FileNotFoundError(
                f"背景画像を読み込めません: "
                f"{map_data.background_file}"
            )

        if collision_image is None:
            raise FileNotFoundError(
                f"当たり判定画像を読み込めません: "
                f"{map_data.collision_file}"
            )

        self.collision_map = CollisionMap(collision_image)

        if spawn_position is None:
            spawn_position = map_data.start_position

        # スポーン位置はプレイヤー画像の左上位置
        self.player_image_rect.topleft = spawn_position

        # 当たり判定を画像の足元付近に配置
        self.player_rect.topleft = (
            spawn_position[0] + self.PLAYER_COLLISION_OFFSET[0],
            spawn_position[1] + self.PLAYER_COLLISION_OFFSET[1],
        )

        self.animation_index = 0
        self.animation_timer = 0.0

        # スポーン地点が通行不可の場合は警告する
        if not self.collision_map.is_rect_walkable(self.player_rect):
            print(
                f"警告: マップ {map_name} のスポーン地点 "
                f"{spawn_position} は通行不可です。"
            )

    # --------------------------------------------------
    # プレイヤーアニメーション
    # --------------------------------------------------

    def load_animation_images(self):
        """プレイヤーの方向別アニメーション画像を読み込む。"""

        if self.animation_images:
            return

        for direction in ("up", "down", "left", "right"):
            folder = Path(EXPLORATION_CHARACTER_DIR) / direction

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
                    f"アニメーション画像がありません: {folder}"
                )

            images = []

            for image_path in image_paths:
                image = self.game.image_manager.image(
                    image_path.name,
                    folder,
                    self.PLAYER_SIZE,
                )

                if image is not None:
                    images.append(image)

            if not images:
                raise FileNotFoundError(
                    f"アニメーション画像を読み込めません: {folder}"
                )

            self.animation_images[direction] = images

        self.player_image = self.animation_images["down"][0]

    def update_player_animation(self, dt, moving):
        """移動方向に応じてプレイヤー画像を更新する。"""

        images = self.animation_images[self.player_direction]

        if not moving:
            self.animation_index = 0
            self.animation_timer = 0.0
            self.player_image = images[0]
            return

        self.animation_timer += dt

        if self.animation_timer >= self.animation_interval:
            self.animation_timer -= self.animation_interval
            self.animation_index = (
                self.animation_index + 1
            ) % len(images)

        self.player_image = images[self.animation_index]

    # --------------------------------------------------
    # プレイヤー移動
    # --------------------------------------------------

    def move_player(self, dx, dy, dt):
        """当たり判定を確認しながらプレイヤーを移動する。"""

        if dx == 0 and dy == 0:
            return False

        # 斜め移動が速くならないようにする
        length = math.hypot(dx, dy)

        if length > 0:
            dx /= length
            dy /= length

        move_x = round(dx * self.PLAYER_SPEED * dt)
        move_y = round(dy * self.PLAYER_SPEED * dt)

        moving = False

        # 横方向の移動
        if move_x != 0:
            candidate = self.player_rect.copy()
            candidate.x += move_x

            if self.collision_map.is_rect_walkable(candidate):
                self.player_rect.x = candidate.x
                moving = True

        # 縦方向の移動
        if move_y != 0:
            candidate = self.player_rect.copy()
            candidate.y += move_y

            if self.collision_map.is_rect_walkable(candidate):
                self.player_rect.y = candidate.y
                moving = True

        # 当たり判定の位置に合わせて画像の描画位置を更新
        self.player_image_rect.topleft = (
            self.player_rect.x - self.PLAYER_COLLISION_OFFSET[0],
            self.player_rect.y - self.PLAYER_COLLISION_OFFSET[1],
        )

        return moving

    # --------------------------------------------------
    # 敵と心音BGM
    # --------------------------------------------------

    def sync_heartbeat_bgm(self):
        """敵の有無に応じて心音BGMを再生・停止する。"""

        has_enemy = bool(self.enemy_manager.enemies)

        if has_enemy:
            self.game.audio_manager.play_bgm(
                self.HEARTBEAT_BGM
            )
        else:
            self.game.audio_manager.stop_bgm()

    def check_enemy_collision(self):
        """プレイヤーが敵に接触したか確認する。"""

        for enemy in self.enemy_manager.enemies:
            if self.player_rect.colliderect(enemy.rect):
                self.start_death_sequence()
                return

    # --------------------------------------------------
    # 暗転・リスタート
    # --------------------------------------------------

    def start_death_sequence(self):
        """接触時に暗転処理を開始する。"""

        if self.is_dying:
            return

        self.is_dying = True
        self.fade_alpha = 0
        self.fade_direction = 1
        self.reset_done = False

    def restart_game(self):
        """初期マップに戻り、アイテムと敵を再設定する。"""

        start_map = "syosai"
        start_position = (
            self.map_manager.maps[start_map].start_position
        )

        # アイテム数と回収状況をリセット
        self.item_manager.reset()

        # 初期マップに戻す
        self.load_map(
            start_map,
            spawn_position=start_position,
        )

        # アイテムを再配置
        collision_maps = self.create_collision_maps()

        self.item_manager.spawn_items(
            collision_maps,
            self.map_manager.current_map_name,
            self.player_rect,
        )

        # 敵を再配置
        self.enemy_manager.enter_map(
            self.collision_map,
            self.player_rect,
        )

        # 敵の有無に合わせて心音を更新
        self.sync_heartbeat_bgm()

        self.reset_done = True

    def update_death_sequence(self, dt):
        """画面を暗転させ、リスタート後に明転する。"""

        if self.fade_direction == 1:
            # 暗転
            self.fade_alpha = min(
                255,
                self.fade_alpha + self.FADE_SPEED * dt,
            )

            if self.fade_alpha >= 255 and not self.reset_done:
                self.restart_game()
                self.fade_direction = -1

        elif self.fade_direction == -1:
            # 明転
            self.fade_alpha = max(
                0,
                self.fade_alpha - self.FADE_SPEED * dt,
            )

            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_direction = 0
                self.is_dying = False
                self.reset_done = False

    # --------------------------------------------------
    # マップ移動・扉のSE
    # --------------------------------------------------

    def check_map_transition(self):
        """プレイヤーが現在のマップの移動領域にいるか調べる。"""

        current_map = self.map_manager.current_map_name

        for transition in self.map_transitions:
            if transition["from_map"] != current_map:
                continue

            if self.player_rect.colliderect(transition["area"]):
                return transition

        return None

    def transition_to_map(self, transition):
        """扉のSEを鳴らし、移動先のマップに切り替える。"""

        from_map = self.map_manager.current_map_name
        entrance_id = transition["entrance_id"]

        destination = self.map_manager.get_transition(
            from_map,
            entrance_id,
        )

        if destination is None:
            print(
                f"移動先が定義されていません: "
                f"{from_map}, {entrance_id}"
            )
            return

        # 扉を開ける音
        self.game.audio_manager.play_se(
            self.DOOR_OPEN_SE
        )

        # 移動先に切り替える
        self.load_map(
            destination["target_map"],
            spawn_position=destination["spawn_position"],
        )

        # 移動先の敵を設定する
        self.enemy_manager.enter_map(
            self.collision_map,
            self.player_rect,
        )

        # 扉を閉める音
        self.game.audio_manager.play_se(
            self.DOOR_CLOSE_SE
        )

        # 移動先の敵の有無に合わせてBGMを更新
        self.sync_heartbeat_bgm()

    # --------------------------------------------------
    # ゲーム更新
    # --------------------------------------------------

    def update(self, dt):
        """毎フレームの更新処理。"""

        # 暗転中は移動などを受け付けない
        if self.is_dying:
            self.update_death_sequence(dt)
            return

        # アイテムをすべて集めたら終了状態を維持する
        if self.item_manager.game_cleared:
            return

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        if dx < 0:
            self.player_direction = "left"
        elif dx > 0:
            self.player_direction = "right"
        elif dy < 0:
            self.player_direction = "up"
        elif dy > 0:
            self.player_direction = "down"

        moving = self.move_player(dx, dy, dt)
        self.update_player_animation(dt, moving)

        # 敵をプレイヤーに向けて移動させる
        self.enemy_manager.update(
            dt,
            self.player_rect,
        )

        # 敵に接触した場合はリスタート処理へ
        self.check_enemy_collision()

        if self.is_dying:
            return

        # アイテム回収
        self.item_manager.collect_items(
            self.player_rect,
            self.map_manager.current_map_name,
        )

        # 敵の有無に合わせてBGMを同期
        self.sync_heartbeat_bgm()

    # --------------------------------------------------
    # 描画
    # --------------------------------------------------

    def draw(self, screen):
        screen.fill(BG_COLOR)

        offset_x, offset_y = self.get_map_draw_offset(screen)

        # 背景
        if self.background_image is not None:
            screen.blit(
                self.background_image,
                (offset_x, offset_y),
            )

        # アイテム
        self.item_manager.draw_items(
            screen,
            self.map_manager.current_map_name,
            offset_x,
            offset_y,
        )

        # 敵
        self.enemy_manager.draw(
            screen,
            offset_x,
            offset_y,
        )

        # プレイヤー
        if self.player_image is not None:
            screen.blit(
                self.player_image,
                (
                    self.player_image_rect.x + offset_x,
                    self.player_image_rect.y + offset_y,
                ),
            )

        # 扉にインタラクトできる範囲にいる場合だけ「！」を表示
        transition = self.check_map_transition()
        if transition is not None:
            interact_surface = self.font.render(
                "！",
                True,
                (255, 230, 0),
            )
            interact_rect = interact_surface.get_rect(
                midbottom=(
                    self.player_image_rect.centerx + offset_x,
                    self.player_image_rect.top + offset_y - 4,
                )
            )
            screen.blit(interact_surface, interact_rect)

        # UIは画面固定位置に描画
        item_text = (
            f"アイテム: {self.item_manager.collected_count}"
            f" / {self.item_manager.item_count}"
        )

        item_surface = self.font.render(
            item_text,
            True,
            (255, 255, 255),
        )
        screen.blit(item_surface, (20, 20))

        # ゲームクリア表示
        if self.item_manager.game_cleared:
            clear_surface = self.font.render(
                "GAME CLEAR",
                True,
                (255, 255, 0),
            )
            clear_rect = clear_surface.get_rect(
                center=(screen.get_width() // 2, screen.get_height() // 2)
            )
            screen.blit(clear_surface, clear_rect)

        # 暗転
        if self.is_dying:
            overlay = pygame.Surface(
                screen.get_size(),
                pygame.SRCALPHA,
            )
            overlay.fill((0, 0, 0, int(self.fade_alpha)))
            screen.blit(overlay, (0, 0))

    # --------------------------------------------------
    # イベント処理
    # --------------------------------------------------

    def handle_event(self, event):
        """キー入力などのイベントを処理する。"""

        if self.is_dying:
            return

        if event.type != pygame.KEYDOWN:
            return

        if event.key not in (pygame.K_SPACE, pygame.K_RETURN):
            return

        # プレイヤーが扉の移動領域にいるか調べる
        transition = self.check_map_transition()

        if transition is not None:
            self.transition_to_map(transition)

    def get_map_draw_offset(self, screen):
        """マップを画面中央に配置するための描画オフセットを返す。"""
        if self.background_image is None:
            return 0, 0

        screen_width, screen_height = screen.get_size()
        map_width, map_height = self.background_image.get_size()

        offset_x = (screen_width - map_width) // 2
        offset_y = (screen_height - map_height) // 2

        return offset_x, offset_y