#ui/menu.py

import pygame
from settings.constants import *
from ui.colors import colors

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 28)
        self.start_button = pygame.Rect(
            screen.get_width() // 2 - 100,
            screen.get_height() - 70,
            200, 50
        )

    def draw_map_preview(self, map_controller):
        #малює повну мапу лабіринту у стартовому режимі гри

        self.screen.fill(colors["BLACK"])

        for x in range(map_width):
            for y in range(map_height):
                px, py = x * sector_size, y * sector_size

                pygame.draw.rect(self.screen, colors["YELLOW"], (px, py, sector_size, sector_size))
                walls = map_controller.grid[x][y]['walls']
                t = 5

                if walls['top']:
                    pygame.draw.rect(self.screen, colors["GRAY"], (px, py, sector_size, t))
                if walls['bottom']:
                    pygame.draw.rect(self.screen, colors["GRAY"], (px, py + sector_size - t, sector_size, t))
                if walls['left']:
                    pygame.draw.rect(self.screen, colors["GRAY"], (px, py, t, sector_size))
                if walls['right']:
                    pygame.draw.rect(self.screen, colors["GRAY"], (px + sector_size - t, py, t, sector_size))

                if (x, y) == map_controller.treasure_pos:
                    pygame.draw.circle(
                        self.screen, colors["GREEN"],
                        (px + sector_size // 2, py + sector_size // 2),
                        20
                    )

        pygame.draw.rect(self.screen, colors["WHITE"], self.start_button)
        text = self.font.render("Почати гру", True, colors["BLACK"])
        text_rect = text.get_rect(center=self.start_button.center)
        self.screen.blit(text, text_rect)
