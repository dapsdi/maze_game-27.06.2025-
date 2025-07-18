#core/game.py
import pygame
import settings.constants as const
from map.map_controller import MapController
from entities.player import Player
from core.camera import Camera
from ui.start_screen import show_start_screen

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(const.title)

        # відкриваємо вікно фіксованого розміру
        self.screen = pygame.display.set_mode((const.window_width, const.window_height))

        # обчислюємо розмір тайлу і сектора
        const.tile_px     = min(const.window_width, const.window_height) // const.tile_grid_size
        const.sector_size = const.tile_px * const.tile_grid_size

        #встановлення початкового спавна для гравця(завжди біом рівнин)
        self.map_controller = MapController()

        start_sector = None
        for x in range(const.map_width):
            for y in range(const.map_height):
                if self.map_controller.get_biome((x, y)) == "plains":
                    self.sector = (x, y)
                    break
            if start_sector:
                break
        if start_sector is None:
            start_sector = (0, 0) #якщо не знайдено рівнин, спавнимо у (0, 0)
        
        self.player = Player(start_sector = start_sector)
        self.camera = Camera()
        self.clock = pygame.time.Clock()

        # показуємо стартовий екран із двома кнопками
        show_start_screen(self.screen)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(const.fps) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                  (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

            # отримуємо глобальні стіни поточного сектора
            sx, sy = self.player.get_sector()
            global_walls  = self.map_controller.get_sector_walls((sx, sy))
            tile_walls   = self.map_controller.get_tile_colliders((sx, sy))
            all_walls = global_walls + tile_walls

            # оновлюємо
            self.player.update(dt, all_walls)
            self.camera.update(self.player)

            # малюємо
            self.map_controller.draw_sector(self.screen, (sx, sy))
            self.player.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
