import pygame
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS, TITLE_NAME
from game.paths import ADV_RIRI_DIR
from game.audios import AudioManager
from game.images import ImageManager
from game.states import StateManager

class GameManager():
    def __init__(self):
        pygame.init()
        self.running = True
        self.fullscreen = False

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_caption(TITLE_NAME)
        self.game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.audio_manager = AudioManager()
        self.image_manager = ImageManager()

        icon = self.image_manager.image("riri mini.png", ADV_RIRI_DIR, size=(32, 32))
        if icon is not None:
            pygame.display.set_icon(icon)
        
        self.clock = pygame.time.Clock()
        self.state_manager = StateManager(self)

    def window_to_game_pos(self, pos):
        window_width, window_height = self.screen.get_size()
        scale = min(window_width / SCREEN_WIDTH, window_height / SCREEN_HEIGHT)
        scaled_width = SCREEN_WIDTH * scale
        scaled_height = SCREEN_HEIGHT * scale
        offset_x = (window_width - scaled_width) // 2
        offset_y = (window_height - scaled_height) // 2
        if not (offset_x <= pos[0] <= offset_x + scaled_width and offset_y <= pos[1] <= offset_y + scaled_height):
            return None
        x = (pos[0] - offset_x) / scale
        y = (pos[1] - offset_y) / scale

        return (int(x), int(y))

    def process_event(self, event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            pos = self.window_to_game_pos(event.pos)
            if pos is None:
                return
            attributes = event.dict.copy()
            attributes['pos'] = pos
            if event.type == pygame.MOUSEMOTION:
                window_width, window_height = self.screen.get_size()
                scale = min(window_width / SCREEN_WIDTH, window_height / SCREEN_HEIGHT)
                rel = getattr(event, 'rel', (0, 0))
                attributes['rel'] = (rel[0] / scale, rel[1] / scale)
            event = pygame.event.Event(event.type, attributes)
        self.state_manager.handle_event(event)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    def draw(self):
        self.state_manager.draw(self.game_surface)
        window_width, window_height = self.screen.get_size()
        scale = min(window_width / SCREEN_WIDTH, window_height / SCREEN_HEIGHT)
        scaled_width = max(1, round(SCREEN_WIDTH * scale))
        scaled_height = max(1, round(SCREEN_HEIGHT * scale))
        offset_x = (window_width - scaled_width) // 2
        offset_y = (window_height - scaled_height) // 2
        
        self.screen.fill(BG_COLOR)
        scaled_surface = pygame.transform.scale(self.game_surface, (scaled_width, scaled_height))
        self.screen.blit(scaled_surface, (offset_x, offset_y))
        pygame.display.flip()
        
    def run(self):
        try:
            while self.running:
                dt = min(self.clock.tick(FPS) / 1000, 0.05)
                for event in pygame.event.get():
                    self.process_event(event)
                    if not self.running:
                        break
                if not self.running:
                    break
                self.state_manager.update(dt)
                self.draw()
        finally:
            self.audio_manager.close()
            pygame.quit()