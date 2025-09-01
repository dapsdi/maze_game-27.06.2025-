import pygame
import settings.constants as const
from map.map_controller import MapController
from entities.player import Player
from core.camera import Camera
from ui.start_screen import show_start_screen
from ui.settings_screen import show_settings_screen, load_config

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(const.title)

        self.screen = pygame.display.set_mode((const.window_width, const.window_height))

        const.tile_px     = min(const.window_width, const.window_height) // const.tile_grid_size
        const.sector_size = const.tile_px * const.tile_grid_size

        self.map_controller = MapController()

        start_sector = None
        for x in range(const.map_width):
            for y in range(const.map_height):
                if self.map_controller.get_biome((x, y)) == "plains":
                    start_sector = (x, y)
                    break
            if start_sector:
                break
        if start_sector is None:
            start_sector = (0, 0)

        self.player = Player(start_sector=start_sector)
        self.camera = Camera()
        self.clock = pygame.time.Clock()

        # --- музика ---
        cfg = load_config()
        pygame.mixer.music.load("assets/music/Indigo-Future-Melody.mp3")
        pygame.mixer.music.set_volume(cfg["volume"])
        pygame.mixer.music.play(-1)

        show_start_screen(self.screen)
        self.settings_button = pygame.Rect(const.window_width - 60, 20, 40, 40)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(const.fps) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.settings_button.collidepoint(event.pos):
                        show_settings_screen(self.screen)

            sx, sy = self.player.get_sector()
            global_walls = self.map_controller.get_sector_walls((sx, sy))
            tile_walls   = self.map_controller.get_tile_colliders((sx, sy))
            all_walls    = global_walls + tile_walls

            self.player.update(dt, all_walls)
            self.camera.update(self.player)

            self.map_controller.draw_sector(self.screen, (sx, sy))
            self.player.draw(self.screen)

            pygame.draw.rect(self.screen, (200, 200, 200, 150), self.settings_button)
            pygame.display.flip()

        pygame.quit()
