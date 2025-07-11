import pygame
from settings.constants import sector_size
from ui.menu import resize_to_sector

class EventHandler:
    def __init__(self, game_state, screen):
        self.game_state = game_state
        self.screen = screen

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_state.in_game:
                #якщо гравець натиснув кнопку старту — змінюємо режим
                from ui.menu import start_button
                if start_button.collidepoint(event.pos):
                    self.game_state.in_game = True
                    self.screen = resize_to_sector()
