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
        self.audio_manager = AudioManager()
        self.image_manager = ImageManager()
        self.state_manager = StateManager(self)
        pygame.display.set_icon(self.image_manager.images["riri mini.png", (32, 32)])
        pygame.display.set_caption(TITLE_NAME)
        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            for event in pygame.event.get():
                self.state_manager.handle_event(event)
            self.state_manager.update(dt)
            self.state_manager.draw(self.screen)
        self.audio_manager.close()
        pygame.quit()