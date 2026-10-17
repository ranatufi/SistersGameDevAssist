import sys
from pathlib import Path
import pygame

#素材パスを設定（exeとスクリプト実行でパスが違うため）
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"

#初期値の設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

def main():
    #初期化（データ削除ではなくゲーム起動に必要な最初の処理って意味）
    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.RESIZABLE
    )
    pygame.display.set_caption("UnsealEscape")
    clock = pygame.time.Clock()
    background_color = (0, 0, 0)
    running = True

    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 描画処理
        screen.fill(background_color)

        # 画面を更新
        pygame.display.flip()

        # FPS制御
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()