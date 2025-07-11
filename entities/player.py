#entities/player.py#
import pygame
from settings.constants import *

class Player:
    def __init__(self):
        #гравець стартує у секторі (0,0) на тайлі (1,1), який завжди прохідний
        self.sector = (0, 0)
        self.size = 30
        self.color = (0, 100, 255)

        #координати тайла (1,1) і його центр
        tile_grid_size = 9
        tile_size = sector_size // tile_grid_size
        spawn_x = tile_size * 1 + tile_size // 2
        spawn_y = tile_size * 1 + tile_size // 2

        #спавн гравця в центрі прохідного тайла
        self.rect = pygame.Rect(
            spawn_x - self.size // 2,
            spawn_y - self.size // 2,
            self.size,
            self.size
        )
        self.speed = 4

    def get_sector(self):
        #повертає поточний сектор у вигляді (x,y)
        return self.sector

    def move(self, keys, walls):
        #перевіряє клавіші і переміщує гравця, уникаючи зіткнень зі стінами
        dx = dy = 0
        if keys[pygame.K_LEFT]: dx = -self.speed
        if keys[pygame.K_RIGHT]: dx = self.speed
        if keys[pygame.K_UP]: dy = -self.speed
        if keys[pygame.K_DOWN]: dy = self.speed

        #рухаємо по осі x
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0: self.rect.right = wall.left
                if dx < 0: self.rect.left = wall.right

        #рухаємо по осі y
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0: self.rect.bottom = wall.top
                if dy < 0: self.rect.top = wall.bottom

    def check_collision(self, dx, dy, walls, tile_colliders):
        #перевіряє зіткнення з усіма стінами сектора
        future_rect = self.rect.move(dx, dy)
        for wall in walls + tile_colliders:
            if future_rect.colliderect(wall):
                return True
        return False

    def draw(self, screen):
        #малює гравця у секторі
        pygame.draw.rect(screen, self.color, self.rect)
