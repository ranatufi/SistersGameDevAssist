import pygame
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE_NAME
from game.audios import AudioManager
from game.images import ImageManager
from game.states import StateManager

class GameManager():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.RESIZABLE
        )
        self.audio = AudioManager()
        self.image = ImageManager()
        self.state = StateManager(self)
        pygame.display.set_icon(self.image.images["riri mini.png", (32, 32)])
        pygame.display.set_caption(TITLE_NAME)
        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            for event in pygame.event.get():
                self.state.handle_event(event)
            self.state.update(dt)
            self.state.draw(self.screen)
        self.audio.close()
        pygame.quit()