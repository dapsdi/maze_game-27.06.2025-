#core/game.py#
import pygame
from settings.constants import *
from entities.player import Player
from map.map import GameMap
from ui.button import draw_button
from ui.colors import colors
from ui.settings_menu import SettingsMenu

class Game:
    def __init__(self):
        self.full_screen = True
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.button_font = pygame.font.SysFont(None, 28)

        self.start_button = pygame.Rect(300, 720, 200, 50)
        self.settings_button = pygame.Rect(750, 10, 40, 40)  # невидима кнопка
        self.in_game = False
        self.in_settings = False

        self.player = Player()
        self.map = GameMap()
        self.settings_menu = SettingsMenu()

        self.start_image = pygame.image.load("pictures/start_screen.png").convert()
        self.start_image = pygame.transform.scale(self.start_image, (800, 800))

        self.pixel_scale = 6
        low_res = sector_size // self.pixel_scale
        self.buffer = pygame.Surface((low_res, low_res))

    def run(self):
        running = True
        while running:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not self.in_game:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.start_button.collidepoint(event.pos):
                            self.in_game = True
                            self.full_screen = False
                            self.screen = pygame.display.set_mode((sector_size, sector_size))
                            pygame.display.set_caption(title)
                        elif self.settings_button.collidepoint(event.pos):
                            self.in_settings = not self.in_settings

            if not self.in_game:
                self.draw_placeholder()
                continue

            keys = pygame.key.get_pressed()
            sector = self.player.get_sector()
            walls = self.map.get_walls(sector)
            tile_colliders = self.map.get_tile_colliders(sector)
            chests = self.map.get_chests(sector)

            self.player.move(keys, walls + tile_colliders)

            if keys[pygame.K_f]:
                self.map.try_collect_chest(sector, self.player.rect)

            self.handle_sector_transition()

            #малюємо весь кадр на buffer
            #у buffer розміром low_res x low_res
            self.buffer.fill(colors["BLACK"])
            #малюємо сектор
            #але draw_sector очікує full-res розміри, тому потрібно масштабувати координати всередині buffer:
            #найпростіше намалювати на full_surface а потім up/down scale:
            full = pygame.Surface((sector_size, sector_size))
            full.fill(colors["BLACK"])
            self.map.draw_current_sector(full, sector)
            self.player.draw(full)
            #downscale -> upscale
            small = pygame.transform.scale(full, self.buffer.get_size())
            pixelated = pygame.transform.scale(small, (sector_size, sector_size))
            #переносимо на екран
            self.screen.blit(pixelated, (0, 0))

            pygame.display.flip()

    def draw_placeholder(self):
        self.screen.blit(self.start_image, (0, 0))
        draw_button(self.screen, self.start_button, "Почати гру", self.button_font)
        if self.in_settings:
            self.settings_menu.draw(self.screen)
        pygame.display.flip()

    def handle_sector_transition(self):
        sector_x, sector_y = self.player.get_sector()
        transitioned = False

        if self.player.rect.left < 0 and sector_x > 0:
            sector_x -= 1
            self.player.rect.right = sector_size
            transitioned = True
        elif self.player.rect.right > sector_size and sector_x < map_width - 1:
            sector_x += 1
            self.player.rect.left = 0
            transitioned = True

        if self.player.rect.top < 0 and sector_y > 0:
            sector_y -= 1
            self.player.rect.bottom = sector_size
            transitioned = True
        elif self.player.rect.bottom > sector_size and sector_y < map_height - 1:
            sector_y += 1
            self.player.rect.top = 0
            transitioned = True

        if transitioned:
            self.player.sector = (sector_x, sector_y)
