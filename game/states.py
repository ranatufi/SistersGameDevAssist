import pygame
from game.paths import ADV_BACKGROUND_DIR, ADV_RIRI_DIR
from game.constants import BG_COLOR, T_COLOR, A_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, PROLOGUE_TEXT, STORY_TEXT
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

        self.title_image = None
        self.title_surface = None
        self.play_surface = None
        self.play_rect = None
    
    def enter(self):
        self.title_image = self.game.image_manager.image("taitoru.png", ADV_BACKGROUND_DIR, (SCREEN_WIDTH, SCREEN_HEIGHT),)
        self.title_font = pygame.font.SysFont("Georgia", 70, bold=True)
        self.play_surface = self.title_font.render("Play", True, T_COLOR)
        self.play_rect = self.play_surface.get_rect(center=(SCREEN_WIDTH // 2, 400))

    def draw(self, screen):
        if self.title_image is not None:
            screen.blit(self.title_image, (0, 0))
        if self.play_surface is not None:
            screen.blit(self.play_surface, self.play_rect)
    
    def exit(self):
        pass

    def update(self, dt):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def handle_click(self, pos):
        if self.play_rect and self.play_rect.collidepoint(pos):
            #self.state_manager.change_state(GameState.PROLOGUE)
            self.state_manager.change_state(GameState.STORY) #テスト

class PrologueState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)

        self.scroll_y = 0.0
        self.target_y = SCREEN_HEIGHT * 0.46

        self.scroll_speed = 100.0
        self.scroll_finished = False
        self.text_surface = None
        self.arrow_surface = None
        self.arrow_rect = None

        self.prologue_text = PROLOGUE_TEXT

    def create_text_surface(self, text, font, color, max_width):
        lines = []
        for paragraph_line in text.split("\n"):
            if not paragraph_line:
                lines.append("")
                continue
            current_line = ""
            for char in paragraph_line:
                candidate = current_line + char
                if current_line and font.size(candidate)[0] > max_width:
                    lines.append(current_line)
                    current_line = char
                else:
                    current_line = candidate
            if current_line:
                lines.append(current_line)
        
        line_height = font.get_linesize() + 8
        surface_height = max(1, len(lines) * line_height)
        surface = pygame.Surface((max_width, surface_height), pygame.SRCALPHA)
        for index, line in enumerate(lines):
            if not line:
                continue
            rendered_line = font.render(line, True, color)
            rect = rendered_line.get_rect(centerx=max_width // 2, y=index * line_height)
            surface.blit(rendered_line, rect)
        
        return surface
    
    def enter(self):
        self.game.audio_manager.play_bgm("死神のリスト.mp3")
        self.font = pygame.font.SysFont("Yu Mincho", 40, bold=True)
        self.english_font = pygame.font.SysFont("Georgia", 40, bold=True)
        self.arrow_font = pygame.font.SysFont("Yu Mincho", 60, bold=True)

        self.text_surface = self.create_text_surface(self.prologue_text, self.font, T_COLOR, SCREEN_WIDTH - 80)
        self.arrow_surface = self.arrow_font.render("➡", True, A_COLOR)
        self.arrow_rect = self.arrow_surface.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.83)))
        self.scroll_y = (SCREEN_HEIGHT + self.text_surface.get_height() // 2)
        self.scroll_finished = False

    def exit(self):
        pass
    
    def update(self, dt):
        if self.scroll_finished:
            return
        self.scroll_y -= self.scroll_speed * dt
        if self.scroll_y <= self.target_y:
            self.scroll_y = self.target_y
            self.scroll_finished = True
    
    def draw(self, screen):
        screen.fill(BG_COLOR)
        if self.text_surface is not None:
            text_rect = self.text_surface.get_rect(
                center=(SCREEN_WIDTH // 2, round(self.scroll_y)))
            screen.blit(self.text_surface, text_rect)
        if self.scroll_finished and self.arrow_surface is not None:
            screen.blit(self.arrow_surface, self.arrow_rect)
    
    def handle_event(self, event):
        if (self.scroll_finished and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if self.arrow_rect and self.arrow_rect.collidepoint(event.pos):
                self.handle_click(event.pos)

    def handle_click(self, pos):
        self.state_manager.change_state(GameState.STORY)

class StoryState(BaseState):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)

        self.story_lines = list(STORY_TEXT)
        self.current_line_index = 0
        self.current_text = ""

        self.background = None
        self.character = None
        self.frame = None

        self.text_rect = pygame.Rect(180, 550, SCREEN_WIDTH / 1.5, 100)
        self.next_rect = pygame.Rect(SCREEN_WIDTH * 0.75, 640, 40, 35)

        self.display_text = ""

    def show_current_line(self):
        if self.current_line_index >= len(self.story_lines):
            self.state_manager.change_state(GameState.EXPLORATION)
            return
        self.current_text = self.story_lines[self.current_line_index]
        self.char_index = 0
        self.display_text = ""
        self.type_timer = 0.0
        self.auto_timer = 0.0
        self.is_typing = True
    
    def enter(self):
        self.game.audio_manager.play_bgm("死神のリスト.mp3")
        self.background = self.game.image_manager.image("haikei.png", ADV_BACKGROUND_DIR, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.character = self.game.image_manager.image("riri.PNG", ADV_RIRI_DIR, (1200, 1200))
        self.frame = self.game.image_manager.image("kakomi.png", ADV_BACKGROUND_DIR, (800, 200))
        self.text_font = pygame.font.SysFont("msmincho", 26, bold=True)
        self.next_font = pygame.font.SysFont("msgothic", 24, bold=True)

        self.current_line_index = 0
        self.show_current_line()

        self.is_auto = False
        self.is_typing = False

        self.char_index = 0
        self.type_timer = 0.0
        self.auto_timer = 0.0

        self.type_interval = 0.06
        self.auto_interval = 2.5

        self.auto_rect = pygame.Rect(850, 20, 60, 30)
        self.skip_rect = pygame.Rect(920, 20, 60, 30)

        self.button_font = pygame.font.SysFont("msgothic", 18, bold=True)

        self.current_line_index = 0
        self.is_auto = False
        self.is_typing = False
        self.display_text = ""
        self.char_index = 0
        self.type_timer = 0.0
        self.auto_timer = 0.0

        self.show_current_line()
    
    def exit(self):
        pass
    
    def update(self, dt):
        if self.is_typing:
            self.type_timer += dt
            while self.type_timer >= self.type_interval:
                self.type_timer -= self.type_interval
                if self.char_index < len(self.current_text):
                    self.char_index += 1
                    self.display_text = self.current_text[:self.char_index]
                else:
                    self.is_typing = False
                    self.auto_timer = 0.0
                    break

        elif self.is_auto:
            self.auto_timer += dt
            if self.auto_timer >= self.auto_interval:
                self.current_line_index += 1
                self.show_current_line()
    
    def draw(self, screen):
        if self.background is not None:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BG_COLOR)
        if self.character is not None:
            character_rect = self.character.get_rect(center=(800, 520))
            screen.blit(self.character, character_rect)
        if self.frame is not None:
            frame_rect = self.frame.get_rect(center=(SCREEN_WIDTH // 2, 600))
            screen.blit(self.frame, frame_rect)
        else:
            pygame.draw.rect(screen, (17, 17, 17), (125, 450, 550, 125))
            pygame.draw.rect(screen, T_COLOR, (125, 450, 550, 125), 1)

        self.draw_wrapped_text(screen, self.display_text, self.text_font, T_COLOR, self.text_rect)
        pygame.draw.rect(screen, (17, 17, 17), self.next_rect)

        arrow_surface = self.next_font.render("▼", True, T_COLOR)
        arrow_rect = arrow_surface.get_rect(center=self.next_rect.center)
        screen.blit(arrow_surface, arrow_rect)

        auto_color = (100, 100, 100) if self.is_auto else (17, 17, 17)
        pygame.draw.rect(screen, auto_color, self.auto_rect)
        pygame.draw.rect(screen, T_COLOR, self.auto_rect, 1)
        auto_surface = self.button_font.render("AUTO", True, T_COLOR)
        screen.blit(auto_surface, auto_surface.get_rect(center=self.auto_rect.center))

        pygame.draw.rect(screen, (17, 17, 17), self.skip_rect)
        pygame.draw.rect(screen, T_COLOR, self.skip_rect, 1)
        skip_surface = self.button_font.render("SKIP", True, T_COLOR)
        screen.blit(skip_surface, skip_surface.get_rect(center=self.skip_rect.center))

    def draw_wrapped_text(self, screen, text, font, color, rect):
        lines = []

        for paragraph in text.split("\n"):
            current_line = ""
            for char in paragraph:
                candidate = current_line + char
                if font.size(candidate)[0] > rect.width:
                    lines.append(current_line)
                    current_line = char
                else:
                    current_line = candidate
            lines.append(current_line)

        line_height = font.get_linesize()
        total_height = len(lines) * line_height
        y = rect.centery - total_height // 2

        for line in lines:
            surface = font.render(line, True, color)
            line_rect = surface.get_rect(centerx=rect.centerx, y=y)
            screen.blit(surface, line_rect)
            y += line_height
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)
    
    def handle_click(self, pos):
        if self.skip_rect.collidepoint(pos):
            self.state_manager.change_state(GameState.EXPLORATION)
            return
        if self.auto_rect.collidepoint(pos):
            self.is_auto = not self.is_auto
            self.auto_timer = 0.0
            return
        if self.next_rect.collidepoint(pos):
            if self.is_typing:
                self.display_text = self.current_text
                self.char_index = len(self.current_text)
                self.is_typing = False
                self.auto_timer = 0.0
            else:
                self.current_line_index += 1
                self.show_current_line()

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