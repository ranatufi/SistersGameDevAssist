import pygame
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR, TITLE_NAME
from game.assets import AssetsManager
from game.states import GameState

class GameManager():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.RESIZABLE
        )
        self.assets = AssetsManager()
        pygame.display.set_icon(self.assets.images["riri mini.png", (32, 32)])
        pygame.display.set_caption(TITLE_NAME)
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = GameState.TITLE

    def handle_event(self, event):
        match event.type:
            case pygame.QUIT:
                self.running = False
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_click(event.pos)
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.running = False
                    case pygame.K_F11:
                        pygame.display.toggle_fullscreen()

    def handle_click(self, pos):
        match self.state:
            case GameState.TITLE:
                self.state = GameState.PROLOGUE
            case GameState.PROLOGUE:
                self.state = GameState.STORY
            case GameState.STORY:
                self.state = GameState.EXPLORATION
            case GameState.EXPLORATION:
                pass

    def update(self, dt):
        match self.state:
            case GameState.TITLE:
                pass
            case GameState.PROLOGUE:
                pass
            case GameState.STORY:
                pass
            case GameState.EXPLORATION:
                pass

    def draw(self):
        self.screen.fill(BG_COLOR)
        match self.state:
            case GameState.TITLE:
                pass
            case GameState.PROLOGUE:
                pass
            case GameState.STORY:
                pass
            case GameState.EXPLORATION:
                pass
        pygame.display.flip()
    
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()

        #self.audio.close()
        pygame.quit()