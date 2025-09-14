import pygame
import json
import settings.constants as const
from ui import colors

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"volume": 0.5, "fps": 60}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f)

def show_admin_menu(screen, player):
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont(None, const.SETTINGS_TITLE_FONT_SIZE)
    font = pygame.font.SysFont(None, const.SETTINGS_FONT_SIZE)
    
    #розміри меню
    menu_width = 500
    menu_height = 450
    menu_x = (screen.get_width() - menu_width) // 2
    menu_y = (screen.get_height() - menu_height) // 2
    
    #кнопки адмінського меню
    buttons = [
        {"rect": pygame.Rect(menu_x + 50, menu_y + 80, 400, 50), "text": "Toggle No-Clip", "action": "noclip"},
        {"rect": pygame.Rect(menu_x + 50, menu_y + 150, 400, 50), "text": "Set Speed to x3", "action": "speed"},
        {"rect": pygame.Rect(menu_x + 50, menu_y + 220, 400, 50), "text": "Add 100 Flowers", "action": "add_flowers"},
        {"rect": pygame.Rect(menu_x + 50, menu_y + 290, 400, 50), "text": "Add All Potions", "action": "add_potions"},
        {"rect": pygame.Rect(menu_x + 50, menu_y + 360, 400, 50), "text": "Close Admin Menu", "action": "close"}
    ]
    
    running = True
    while running:
        dt = clock.tick(const.fps) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for button in buttons:
                    if button["rect"].collidepoint(mx, my):
                        if button["action"] == "noclip":
                            player.noclip = not player.noclip
                        elif button["action"] == "speed":
                            player.speed = 3 * const.PLAYER_SPEED
                            player.base_speed = 3 * const.PLAYER_SPEED
                        elif button["action"] == "add_flowers":
                            player.flowers += 100
                        elif button["action"] == "add_potions":
                            for potion_type in player.potion_inventory.inventory:
                                player.potion_inventory.inventory[potion_type] += 5
                        elif button["action"] == "close":
                            return
        
        #малюємо фон меню
        pygame.draw.rect(screen, const.SETTINGS_MENU_BG_COLOR, (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(screen, const.SETTINGS_MENU_BORDER_COLOR, (menu_x, menu_y, menu_width, menu_height), const.SETTINGS_MENU_BORDER_WIDTH)
        
        #заголовок
        title = title_font.render("Admin Menu", True, colors.colors["WHITE"])
        screen.blit(title, (menu_x + (menu_width - title.get_width()) // 2, menu_y + 20))
        
        #статус noclip - перевіряємо, чи є атрибут noclip у гравця
        if hasattr(player, 'noclip'):
            status_text = font.render(f"No-Clip: {'ON' if player.noclip else 'OFF'}", True, colors.colors["YELLOW"])
        else:
            status_text = font.render("No-Clip: OFF", True, colors.colors["YELLOW"])
        screen.blit(status_text, (menu_x + 50, menu_y + 40))
        
        #кнопки
        mx, my = pygame.mouse.get_pos()
        for button in buttons:
            hovered = button["rect"].collidepoint(mx, my)
            color = const.SETTINGS_BUTTON_HOVER_COLOR if hovered else const.SETTINGS_BUTTON_COLOR
            
            pygame.draw.rect(screen, color, button["rect"])
            pygame.draw.rect(screen, const.SETTINGS_BUTTON_BORDER_COLOR, button["rect"], 2)
            
            text = font.render(button["text"], True, colors.colors["WHITE"])
            screen.blit(text, (button["rect"].x + 10, button["rect"].y + 15))
        
        pygame.display.flip()
    
    return None

def show_password_dialog(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, const.SETTINGS_FONT_SIZE)
    
    #розміри діалогового вікна
    dialog_width = 400
    dialog_height = 200
    dialog_x = (screen.get_width() - dialog_width) // 2
    dialog_y = (screen.get_height() - dialog_height) // 2
    
    password_input = ""
    active = True
    
    running = True
    while running:
        dt = clock.tick(const.fps) / 1000
        
        #прозорий фон
        s = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        screen.blit(s, (0, 0))
        
        #малюємо фон діалогового вікна
        pygame.draw.rect(screen, const.SETTINGS_MENU_BG_COLOR, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(screen, const.SETTINGS_MENU_BORDER_COLOR, (dialog_x, dialog_y, dialog_width, dialog_height), const.SETTINGS_MENU_BORDER_WIDTH)
        
        #заголовок
        title = font.render("Enter Admin Password", True, colors.colors["WHITE"])
        screen.blit(title, (dialog_x + (dialog_width - title.get_width()) // 2, dialog_y + 20))
        
        #поле для вводу пароля
        input_rect = pygame.Rect(dialog_x + 50, dialog_y + 80, dialog_width - 100, 40)
        pygame.draw.rect(screen, const.SETTINGS_SLIDER_BG_COLOR, input_rect)
        pygame.draw.rect(screen, const.SETTINGS_SLIDER_BORDER_COLOR, input_rect, 2)
        
        #відображення пароля (з зірочками)
        display_text = "*" * len(password_input)
        if active:
            display_text += "_"  #курсор
        text_surface = font.render(display_text, True, colors.colors["WHITE"])
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))
        
        #кнопки
        ok_rect = pygame.Rect(dialog_x + 100, dialog_y + 140, 80, 40)
        cancel_rect = pygame.Rect(dialog_x + 220, dialog_y + 140, 80, 40)
        
        pygame.draw.rect(screen, const.SETTINGS_BUTTON_APPLY_COLOR, ok_rect)
        pygame.draw.rect(screen, const.SETTINGS_BUTTON_BORDER_COLOR, ok_rect, 2)
        screen.blit(font.render("OK", True, colors.colors["WHITE"]), (ok_rect.x + 25, ok_rect.y + 10))
        
        pygame.draw.rect(screen, const.SETTINGS_BUTTON_CLOSE_COLOR, cancel_rect)
        pygame.draw.rect(screen, const.SETTINGS_BUTTON_BORDER_COLOR, cancel_rect, 2)
        screen.blit(font.render("Cancel", True, colors.colors["WHITE"]), (cancel_rect.x + 10, ok_rect.y + 10))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN:
                    return password_input == "1292"
                elif event.key == pygame.K_BACKSPACE:
                    password_input = password_input[:-1]
                else:
                    #додаємо тільки цифри
                    if event.unicode.isdigit():
                        password_input += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if ok_rect.collidepoint(mx, my):
                    return password_input == "1292"
                elif cancel_rect.collidepoint(mx, my):
                    return False
                elif input_rect.collidepoint(mx, my):
                    active = True
                else:
                    active = False
    
    return False

def show_settings_screen(screen, player=None):
    cfg = load_config()
    title_font = pygame.font.SysFont(None, const.SETTINGS_TITLE_FONT_SIZE)
    font = pygame.font.SysFont(None, const.SETTINGS_FONT_SIZE)
    small_font = pygame.font.SysFont(None, const.SETTINGS_SMALL_FONT_SIZE)
    
    #розміри меню
    menu_x = (screen.get_width() - const.SETTINGS_MENU_WIDTH) // 2
    menu_y = (screen.get_height() - const.SETTINGS_MENU_HEIGHT) // 2
    
    #кнопки
    apply_rect = pygame.Rect(menu_x + const.SETTINGS_MENU_PADDING, 
                            menu_y + const.SETTINGS_MENU_HEIGHT - const.SETTINGS_BUTTON_BOTTOM_MARGIN - const.SETTINGS_BUTTON_HEIGHT, 
                            const.SETTINGS_BUTTON_WIDTH, const.SETTINGS_BUTTON_HEIGHT)
    close_rect = pygame.Rect(menu_x + const.SETTINGS_MENU_WIDTH - const.SETTINGS_MENU_PADDING - const.SETTINGS_BUTTON_WIDTH, 
                            menu_y + const.SETTINGS_MENU_HEIGHT - const.SETTINGS_BUTTON_BOTTOM_MARGIN - const.SETTINGS_BUTTON_HEIGHT, 
                            const.SETTINGS_BUTTON_WIDTH, const.SETTINGS_BUTTON_HEIGHT)
    admin_rect = pygame.Rect(menu_x + (const.SETTINGS_MENU_WIDTH - const.SETTINGS_BUTTON_WIDTH) // 2, 
                            menu_y + const.SETTINGS_MENU_HEIGHT - const.SETTINGS_BUTTON_BOTTOM_MARGIN - const.SETTINGS_BUTTON_HEIGHT, 
                            const.SETTINGS_BUTTON_WIDTH, const.SETTINGS_BUTTON_HEIGHT)
    
    dragging = None

    running = True
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(const.fps) / 1000
        
        #прозорий фон
        s = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        screen.blit(s, (0, 0))
        
        #малюємо фон меню
        pygame.draw.rect(screen, const.SETTINGS_MENU_BG_COLOR, (menu_x, menu_y, const.SETTINGS_MENU_WIDTH, const.SETTINGS_MENU_HEIGHT))
        pygame.draw.rect(screen, const.SETTINGS_MENU_BORDER_COLOR, (menu_x, menu_y, const.SETTINGS_MENU_WIDTH, const.SETTINGS_MENU_HEIGHT), const.SETTINGS_MENU_BORDER_WIDTH)
        
        #заголовок
        title = title_font.render("Settings", True, colors.colors["WHITE"])
        screen.blit(title, (menu_x + (const.SETTINGS_MENU_WIDTH - title.get_width()) // 2, menu_y + const.SETTINGS_TITLE_TOP_MARGIN))
        
        #слайдери
        #гучність
        volume_y = menu_y + 100
        pygame.draw.rect(screen, const.SETTINGS_SLIDER_BG_COLOR, (menu_x + const.SETTINGS_MENU_PADDING, volume_y, const.SETTINGS_SLIDER_WIDTH, const.SETTINGS_SLIDER_HEIGHT))
        pygame.draw.rect(screen, const.SETTINGS_SLIDER_BORDER_COLOR, (menu_x + const.SETTINGS_MENU_PADDING, volume_y, const.SETTINGS_SLIDER_WIDTH, const.SETTINGS_SLIDER_HEIGHT), 2)
        
        knob_x = menu_x + const.SETTINGS_MENU_PADDING + int(cfg["volume"] * const.SETTINGS_SLIDER_WIDTH)
        pygame.draw.rect(screen, const.SETTINGS_SLIDER_KNOB_COLOR, (knob_x - 5, volume_y - 5, 10, const.SETTINGS_SLIDER_HEIGHT + 10))
        
        volume_text = font.render(f"Volume: {int(cfg['volume'] * 100)}%", True, colors.colors["WHITE"])
        screen.blit(volume_text, (menu_x + const.SETTINGS_MENU_PADDING, volume_y - 30))
        
        #fps
        fps_y = menu_y + 180
        pygame.draw.rect(screen, const.SETTINGS_SLIDER_BG_COLOR, (menu_x + const.SETTINGS_MENU_PADDING, fps_y, const.SETTINGS_SLIDER_WIDTH, const.SETTINGS_SLIDER_HEIGHT))
        pygame.draw.rect(screen, const.SETTINGS_SLIDER_BORDER_COLOR, (menu_x + const.SETTINGS_MENU_PADDING, fps_y, const.SETTINGS_SLIDER_WIDTH, const.SETTINGS_SLIDER_HEIGHT), 2)
        
        fps_ratio = (cfg["fps"] - 30) / (240 - 30)
        knob_x = menu_x + const.SETTINGS_MENU_PADDING + int(fps_ratio * const.SETTINGS_SLIDER_WIDTH)
        pygame.draw.rect(screen, const.SETTINGS_SLIDER_KNOB_COLOR, (knob_x - 5, fps_y - 5, 10, const.SETTINGS_SLIDER_HEIGHT + 10))
        
        fps_text = font.render(f"FPS: {cfg['fps']}", True, colors.colors["WHITE"])
        screen.blit(fps_text, (menu_x + const.SETTINGS_MENU_PADDING, fps_y - 30))
        
        #кнопки
        mx, my = pygame.mouse.get_pos()
        
        #apply button
        apply_hovered = apply_rect.collidepoint(mx, my)
        apply_color = const.SETTINGS_BUTTON_HOVER_COLOR if apply_hovered else const.SETTINGS_BUTTON_APPLY_COLOR
        pygame.draw.rect(screen, apply_color, apply_rect)
        pygame.draw.rect(screen, const.SETTINGS_BUTTON_BORDER_COLOR, apply_rect, 2)
        screen.blit(small_font.render("Apply", True, colors.colors["WHITE"]), (apply_rect.x + 30, apply_rect.y + 15))
        
        #close button
        close_hovered = close_rect.collidepoint(mx, my)
        close_color = const.SETTINGS_BUTTON_HOVER_COLOR if close_hovered else const.SETTINGS_BUTTON_CLOSE_COLOR
        pygame.draw.rect(screen, close_color, close_rect)
        pygame.draw.rect(screen, const.SETTINGS_BUTTON_BORDER_COLOR, close_rect, 2)
        screen.blit(small_font.render("Close", True, colors.colors["WHITE"]), (close_rect.x + 30, close_rect.y + 15))
        
        #admin button
        admin_hovered = admin_rect.collidepoint(mx, my)
        admin_color = const.SETTINGS_BUTTON_HOVER_COLOR if admin_hovered else const.SETTINGS_BUTTON_ADMIN_COLOR
        pygame.draw.rect(screen, admin_color, admin_rect)
        pygame.draw.rect(screen, const.SETTINGS_BUTTON_BORDER_COLOR, admin_rect, 2)
        screen.blit(small_font.render("Admin", True, colors.colors["WHITE"]), (admin_rect.x + 30, admin_rect.y + 15))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if apply_rect.collidepoint(event.pos):
                    save_config(cfg)
                    const.fps = cfg["fps"]
                    #оновлення громкості, якщо є музика
                    if pygame.mixer.get_init():
                        pygame.mixer.music.set_volume(cfg["volume"])
                    running = False
                elif close_rect.collidepoint(event.pos):
                    running = False
                elif admin_rect.collidepoint(event.pos):
                    #відкриваємо діалогове вікно для введення паролю
                    if show_password_dialog(screen) and player:
                        show_admin_menu(screen, player)
                
                #перевірка слайдерів
                if menu_x + const.SETTINGS_MENU_PADDING <= event.pos[0] <= menu_x + const.SETTINGS_MENU_PADDING + const.SETTINGS_SLIDER_WIDTH:
                    if menu_y + 100 <= event.pos[1] <= menu_y + 100 + const.SETTINGS_SLIDER_HEIGHT:
                        dragging = "volume"
                        #оновлення значення гучності
                        rel_x = event.pos[0] - (menu_x + const.SETTINGS_MENU_PADDING)
                        cfg["volume"] = max(0.0, min(1.0, rel_x / const.SETTINGS_SLIDER_WIDTH))
                    elif menu_y + 180 <= event.pos[1] <= menu_y + 180 + const.SETTINGS_SLIDER_HEIGHT:
                        dragging = "fps"
                        #оновлення значення fps
                        rel_x = event.pos[0] - (menu_x + const.SETTINGS_MENU_PADDING)
                        rel = max(0.0, min(1.0, rel_x / const.SETTINGS_SLIDER_WIDTH))
                        cfg["fps"] = int(30 + rel * (240 - 30))

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = None

            elif event.type == pygame.MOUSEMOTION and dragging:
                rel_x = event.pos[0] - (menu_x + const.SETTINGS_MENU_PADDING)
                rel = max(0, min(1, rel_x / const.SETTINGS_SLIDER_WIDTH))
                if dragging == "volume":
                    cfg["volume"] = rel
                elif dragging == "fps":
                    cfg["fps"] = int(30 + rel * (240 - 30))