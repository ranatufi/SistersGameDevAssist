import pygame
from pathlib import Path
from game.constants import BGM_VOLUME, SE_VOLUME
from game.paths import BGM_DIR, SE_DIR, asset_path

class AudioManager:
    def __init__(self):
        self.bgm_started = False
        self.audio_available = True
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"オーディオの初期化に失敗: {e}")
            self.audio_available = False

    def play_bgm(self, filename: str):
        if not self.audio_available or self.bgm_started:
            return
        target_path = asset_path(BGM_DIR, filename)
        try:
            pygame.mixer.music.load(str(target_path))
            pygame.mixer.music.set_volume(BGM_VOLUME)
            pygame.mixer.music.play(-1)
            self.bgm_started = True
        except (pygame.error, OSError) as e:
            print(f"BGMの再生に失敗: {target_path}, 原因: {e}")

    def play_se(self, filename: str):
        if not self.audio_available:
            return
        target_path = asset_path(SE_DIR, filename)
        try:
            sound = pygame.mixer.Sound(str(target_path))
            sound.set_volume(SE_VOLUME)
            sound.play()
        except (pygame.error, OSError) as e:
            print(f"SEの再生に失敗: {target_path}, 原因: {e}")

    def close(self):
        if self.audio_available:
            pygame.mixer.quit()