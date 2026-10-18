import sys
from pathlib import Path

#ディレクトリ定数
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"

#ゲーム内定数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

#色
BG_COLOR = (0, 0, 0) #Background

#名称
TITLE_NAME = "UnsealEscape"