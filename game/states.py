import pygame
from game.paths import ADV_BACKGROUND_DIR
from game.constants import BG_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT
from enum import Enum, auto
from abc import ABC, abstractmethod

class GameState(Enum):
    TITLE = auto()
    PROLOGUE = auto()
    STORY = auto()
    EXPLORATION = auto()

class BaseState(ABC):
    #init、handle_clickは必須ではない
    def __init__(self, game, state_manager):
        self.game = game
        self.state_manager = state_manager

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    def draw_centered_text(self, screen, text, y, font=None, color=(255, 255, 255),):
        if font is None:
            font = self.font
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
        screen.blit(surface, rect)

class StateManager:
    def __init__(self, game, initial_state=GameState.TITLE):
        self.game = game
        self.states = {
            GameState.TITLE: TitleState(game, self),
            GameState.PROLOGUE: PrologueState(game, self),
            GameState.STORY: StoryState(game, self),
            GameState.EXPLORATION: ExplorationState(game, self)
        }
        self.current_state = self.states[initial_state]
        self.current_state.enter()

    def change_state(self, new_state):
        if new_state not in self.states:
            raise ValueError(f"存在しないステート: {new_state}")
        if self.current_state is self.states[new_state]:
            return
        self.current_state.exit()
        self.current_state = self.states[new_state]
        self.current_state.enter()
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            self.current_state.exit()
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.running = False
                self.current_state.exit()
                return
            if event.key == pygame.K_F11:
                self.game.toggle_fullscreen()
                return
        self.current_state.handle_event(event)

    def update(self, dt):
        self.current_state.update(dt)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        self.current_state.draw(screen)

class TitleState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)
    
    def enter(self):
        self.title_image = self.game.image_manager.image("taitoru.png", ADV_BACKGROUND_DIR, (SCREEN_WIDTH, SCREEN_HEIGHT),)

    def draw(self, screen):
        if self.title_image is not None:
            screen.blit(self.title_image, (0, 0))
    
    def exit(self):
        pass

    def update(self, dt):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def handle_click(self, pos):
        self.state_manager.change_state(GameState.PROLOGUE)

class PrologueState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)
    
    def enter(self):
        self.game.audio_manager.play_bgm("死神のリスト.mp3")

    def exit(self):
        pass
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def handle_click(self, pos):
        self.state_manager.change_state(GameState.STORY)

class StoryState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)

    def enter(self):
        self.game.audio_manager.play_bgm("バクテリア.mp3")

    def exit(self):
        pass
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)
    
    def handle_click(self, pos):
        self.state_manager.change_state(GameState.EXPLORATION)

class ExplorationState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)
    
    def enter(self):
        pass
    
    def exit(self):
        pass

    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass
    
    def handle_event(self, event):
        pass