#entities/monster.py#
import pygame
import random
from settings.constants import *

class Enemy:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(400, 300))
        self.speed = 2

    def follow_player(self, target_rect):
        #переміщаємо ворога в напрямку гравця по осях x та y
        if self.rect.x < target_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target_rect.x:
            self.rect.x -= self.speed

        if self.rect.y < target_rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target_rect.y:
            self.rect.y -= self.speed

    def random_move(self, screen):
        #переміщаємо ворога у випадкове місце в межах екрану
        self.rect.x = random.randint(0, screen.get_width() - self.rect.width)
        self.rect.y = random.randint(0, screen.get_height() - self.rect.height)

    def draw(self, screen):
        #малюємо ворога на екрані
        screen.blit(self.image, self.rect)
