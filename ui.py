#ui.py#
import pygame
from settings import colors

def draw_button(screen, rect, text, font, color = colors["DARK_GREEN"]):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, colors["WHITE"])
    screen.blit(text_surface,(rect.x + 20, rect.y + 15))

def show_start_screen(screen, background, button_rect, button_font):
    screen.fill(background)
    draw_button(screen, button_rect, "Почати гру", button_font)
    pygame.display.flip()

def show_game_over(screen, font, caught_count, restart_button, button_font):
    screen.fill(colors["BLACK"])
    text1 = font.render("Гру закінчено!", True, colors["RED"])
    text2 = font.render(f"Вас спіймали {caught_count} разів!", True, colors["WHITE"])

    screen.blit(text1, (screen.get_width() // 2 - text1.get_width() // 2, 180))
    screen.blit(text2, (screen.get_width() // 2 - text2.get_width() // 2, 220))
    draw_button(screen, restart_button, "Почати знову", button_font)
    pygame.display.flip()

    
