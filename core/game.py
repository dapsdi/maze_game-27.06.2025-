#core/game.py#
import pygame
import settings.constants as const
from map.map_controller import MapController
from entities.player import Player
from core.camera import Camera
from ui.start_screen import show_start_screen
from ui.settings_screen import show_settings_screen
from entities.fairy import Fairy

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(const.title)

        # відкриваємо вікно фіксованого розміру
        self.screen = pygame.display.set_mode((const.window_width, const.window_height))

        # обчислюємо розмір тайлу і сектора
        const.tile_px     = min(const.window_width, const.window_height) // const.tile_grid_size
        const.sector_size = const.tile_px * const.tile_grid_size

        # карта і гравець
        self.map_controller = MapController()

        # знайти стартовий сектор у біомі "plains"
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
        self.fairy = Fairy("assets/entities/green blob fairy", self.player)
        self.camera = Camera()
        self.clock = pygame.time.Clock()

        # кнопка налаштувань
        self.setting_button = pygame.Rect(const.window_width - 60, 20, 40, 40)

        # UI анімація квіток
        self.ui_frames = self.map_controller.ui_flower_frames or []
        self.ui_frame_index = 0
        self.ui_timer = 0.0
        self.ui_frame_speed = 0.18

        # стартовий екран
        show_start_screen(self.screen)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(const.fps) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_e:
                        # натискання Е для бафа швидкості
                        #if self.player.activate_speed_boost():
                        self.fairy.activate(7.0)  # фея зʼявляється разом із бустом
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.setting_button.collidepoint(event.pos):
                        show_settings_screen(self.screen)

            # --- Колайдери ---
            sx, sy = self.player.get_sector()
            global_walls  = self.map_controller.get_sector_walls((sx, sy))
            tile_walls    = self.map_controller.get_tile_colliders((sx, sy))
            walls = global_walls + tile_walls

            # --- Оновлення гравця та феї ---
            self.player.update(dt, walls)
            self.fairy.update(dt)

            # --- Логіка переходу між секторами ---
            new_sector = None
            sx, sy = self.player.get_sector()
            if self.player.rect.right < 0 and sx > 0:
                new_sector = (sx - 1, sy)
            elif self.player.rect.left > const.sector_size and sx < const.map_width - 1:
                new_sector = (sx + 1, sy)
            elif self.player.rect.bottom < 0 and sy > 0:
                new_sector = (sx, sy - 1)
            elif self.player.rect.top > const.sector_size and sy < const.map_height - 1:
                new_sector = (sx, sy + 1)

            if new_sector is not None:
                self.player.sector = new_sector
                px, py = self.map_controller.get_safe_transition_point(new_sector)
                self.player.rect.center = (px, py)
                walls = self.map_controller.get_sector_walls(new_sector) + \
                        self.map_controller.get_tile_colliders(new_sector)

            # --- Перевірка збору квітів ---
            collected = self.map_controller.tre_collect_chest(self.player.get_sector(), self.player.rect)
            if collected:
                self.player.flowers += collected

            # --- Камера ---
            self.camera.update(self.player)

            # --- Малюємо сектор, гравця і фею ---
            self.map_controller.draw_sector(self.screen, (self.player.get_sector()))
            self.player.draw(self.screen)
            self.fairy.draw(self.screen)

            # --- Кнопка налаштувань ---
            pygame.draw.rect(self.screen, (200, 200, 200, 80), self.setting_button)

            # --- UI: іконка квітки + лічильник ---
            flowers_count = self.player.flowers
            if self.ui_frames:
                self.ui_timer += dt
                if self.ui_timer >= self.ui_frame_speed:
                    self.ui_timer -= self.ui_frame_speed
                    self.ui_frame_index = (self.ui_frame_index + 1) % len(self.ui_frames)
                frame = self.ui_frames[self.ui_frame_index]
                padding = 8
                self.screen.blit(frame, (padding, padding))
                font = pygame.font.SysFont(None, 28)
                txt = font.render(str(flowers_count), True, (255,255,255))
                self.screen.blit(txt, (padding + frame.get_width() + 8,
                                       padding + (frame.get_height() - txt.get_height()) // 2))
            else:
                font = pygame.font.SysFont(None, 28)
                txt = font.render(str(flowers_count), True, (255,255,255))
                self.screen.blit(txt, (8, 8))

            # --- Підказка для активації бафа ---
            if flowers_count >= 3 and not self.player.boost_active:
                font = pygame.font.SysFont(None, 24)
                hint_txt = font.render("E for speed boost (3x flowers)", True, (255, 255, 100))
                self.screen.blit(hint_txt, (8, 40))

            pygame.display.flip()

        pygame.quit()
