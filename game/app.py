import pygame
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR, TITLE_NAME
#from game.paths import asset_path
from game.states import GameState

class UnsealEscapeGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_icon(icon_image)
        pygame.display.set_caption(TITLE_NAME)
        self.clock = pygame.time.Clock()
        self.background_color = BG_COLOR
        self.running = True

        self.state = GameState.TITLE

    def update(self, dt):
        pass

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    self.running = False
                case pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                case _:
                    pass
    
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)

        #self.audio.close()
        pygame.quit()