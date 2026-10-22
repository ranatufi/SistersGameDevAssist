import pygame
from game.constants import BG_COLOR
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
        if new_state in self.states:
            self.current_state.exit()
            self.current_state = self.states[new_state]
            self.current_state.enter()
        else:
            raise ValueError(f"存在しないステート: {new_state}")
    
    def handle_event(self, event):
        match event.type:
            case pygame.QUIT:
                self.game.running = False
                self.current_state.exit()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.game.running = False
                        self.current_state.exit()
                    case pygame.K_F11:
                        pygame.display.toggle_fullscreen()
            case _:
                self.current_state.handle_event(event)

    def update(self, dt):
        self.current_state.update(dt)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        self.current_state.draw(screen)
        pygame.display.flip()

class TitleState(BaseState):
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def handle_click(self, pos):
        self.state_manager.change_state(GameState.PROLOGUE)

class PrologueState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)
    
    def enter(self):
        self.game.audio.play_bgm("死神のリスト.mp3")

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
        self.game.audio.play_bgm("バクテリア.mp3")

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