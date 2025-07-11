import pygame
from ui.colors import colors

def draw_button(surface, rect, text, font):
    #малює прямокутник і текст в центрі кнопки
    pygame.draw.rect(surface, colors["WHITE"], rect)
    pygame.draw.rect(surface, colors["BLACK"], rect, 2)
    text_surf = font.render(text, True, colors["BLACK"])
    surface.blit(text_surf, text_surf.get_rect(center=rect.center))
