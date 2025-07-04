#player.py#
import pygame
from settings import *

class Player:
    def __init__(self, x, y):

        self.size = 40
        self.x = x
        self.y = y
        self.color = colors["GREEN"]
        self.speed = 5

    def move(self, keys_pressed, walls):
        dx, dy = 0, 0
        if keys_pressed[pygame.K_LEFT]:
            dx = -self.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx = self.speed
        if keys_pressed[pygame.K_UP]:
            dy = -self.speed
        if keys_pressed[pygame.K_DOWN]:
            dy = self.speed

        future_rect = pygame.Rect(self.x + dx, self.y + dy, self.size, self.size)
        #створюємо прямокутник який представляє нову позицію після переміщення
        #якщо нова позиція не перетинається з жодною стіною, то переміщуємо гравця

        if not any(future_rect.colliderect(wall) for wall in walls):
            self.x += dx
            self.y += dy
        
    def draw(self, screen, camera_offset):
        pygame.draw.rect(screen, self.color, 
            (self.x - camera_offset[0], self.y - camera_offset[1], self.size, self.size))

    def get_sector_position(self):
        return(self.x // sector_size, self.y // sector_size)
        #повертає позицію сектору в якому гравець