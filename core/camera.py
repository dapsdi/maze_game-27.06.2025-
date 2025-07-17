#core/camera.py
import pygame
import settings.constants as const

class Camera:
    def __init__(self):
        #ініціалізуємо зсув
        self.offset = (0, 0)

    def update(self, player):
        #розраховуємо зсув у пікселях, базуючись на секторі гравця
        sector_x, sector_y = player.get_sector()
        self.offset = (sector_x * const.sector_size, sector_y * const.sector_size)

    def apply(self, pos):
        #застосовує зсув до будь-якої координати
        x, y = pos
        off_x, off_y = self.offset
        return x - off_x, y - off_y
