import pygame
from settings.constants import colors

def draw_start_screen_elements(screen, button_rect, font):
    #малює кнопку на стартовому екрані
    pygame.draw.rect(screen, colors["DARK_GREEN"], button_rect)
    text = font.render("Почати гру", True, colors["WHITE"])
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
