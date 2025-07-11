#map/map.py#
from map.map_controller import MapController
import pygame
from settings.constants import sector_size

class GameMap:
    def __init__(self):
        #створюємо об'єкт контролера карти
        self.controller = MapController()

    def draw_current_sector(self, screen, sector_pos):
        #малює поточний сектор
        self.controller.draw_sector(screen, sector_pos)

    def get_walls(self, sector_pos):
        #повертає глобальні стіни поточного сектора
        return self.controller.get_sector_walls(sector_pos)

    def get_tile_colliders(self, sector_pos):
        #повертає тайлові колайдери (локальні стіни всередині сектора)
        return self.controller.get_tile_colliders(sector_pos)
    
    def get_chests(self, sector_pos):
        #повертає список скарбів у поточному секторі
        return self.controller.get_chests(sector_pos)
    
    def try_collect_chest(self, sector_pos, player_rect):
        #спробувати зібрати скарб у поточному секторі
        self.controller.tre_collect_chest(sector_pos, player_rect)
    
    def treasure_position(self):
        #повертає координати скарбу
        return self.controller.treasure_pos

    def sectors(self):
        #повертає сектори для малювання
        return self.controller.grid
