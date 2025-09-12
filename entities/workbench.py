#workbench.py#

import pygame

class Workbench:
    def __init__(self, pos):
        # простий квадрат як заглушка
        self.image = pygame.Surface((50, 50))
        self.image.fill((139, 69, 19))  # коричневий
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
