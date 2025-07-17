#ui/start_screen.py
import pygame
import settings.constants as const
from ui.colors import colors

def show_start_screen(screen):
    # фонова картинка
    bg = pygame.image.load("pictures/start_screen.png").convert()
    bg = pygame.transform.scale(bg, (const.window_width, const.window_height))

    btn_w, btn_h = 120, 50
    yes_rect = pygame.Rect(300, 830,btn_w, btn_h)
    no_rect = pygame.Rect(480, 830, btn_w, btn_h)

    font_big = pygame.font.SysFont(None, 48)
    font_btn = pygame.font.SysFont(None, 36)

    waiting = True
    while waiting:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if yes_rect.collidepoint(ev.pos):
                    waiting = False  # старт гри
                elif no_rect.collidepoint(ev.pos):
                    pygame.quit()
                    exit()

        screen.blit(bg, (0,0))


        # кнопки — прозорі, малюємо тільки текст
        yes_txt = font_btn.render("yes", True, colors["WHITE"])
        yes_txt_r = yes_txt.get_rect(center=yes_rect.center)
        screen.blit(yes_txt, yes_txt_r)

        no_txt = font_btn.render("no", True, colors["WHITE"])
        no_txt_r = no_txt.get_rect(center=no_rect.center)
        screen.blit(no_txt, no_txt_r)

        pygame.display.flip()
