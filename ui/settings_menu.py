import pygame
from ui.colors import colors

class SettingsMenu:
    def __init__(self):
        self.surface = pygame.Surface((400, 300))
        self.surface.set_alpha(220) #встановлює рівень прозорості для всієї поверхні
                                    #0 - повністю прозора, 255 - повністю непрозора
                                    #прозорість часто використовується для створення візуальних ефектів
        self.surface.fill(colors["BLACK"])
        self.rect = self.surface.get_rect(center=(400, 400)) #центр вікна

    def draw(self, screen):
        screen.blit(self.surface, self.rect)