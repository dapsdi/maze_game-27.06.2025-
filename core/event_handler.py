#core/event_handler.py#
import pygame
from settings.constants import sector_size, POTION_KEYS
from ui.menu import resize_to_sector

class EventHandler:
    def __init__(self, game_state, screen, player):
        self.game_state = game_state
        self.screen = screen
        self.player = player

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_state.in_game:
                from ui.menu import start_button
                if start_button.collidepoint(event.pos):
                    self.game_state.in_game = True
                    self.screen = resize_to_sector()

            elif event.type == pygame.KEYDOWN:
                # Обробка використання зілль
                if event.key in POTION_KEYS:
                    index = POTION_KEYS.index(event.key)
                    potion_types = list(self.player.inventory.keys())
                    if index < len(potion_types):
                        potion_type = potion_types[index]
                        self.player.use_potion(potion_type)