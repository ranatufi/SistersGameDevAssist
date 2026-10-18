import pygame
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR, TITLE_NAME

class UnsealEscapeGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_caption(TITLE_NAME)
        self.clock = pygame.time.Clock()
        self.background_color = BG_COLOR
        self.running = True

    def update(self, dt):
        pass

    def handle_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.running = False
    
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)

        #self.audio.close()
        pygame.quit()