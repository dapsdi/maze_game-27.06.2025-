import pygame
import json
import settings.constants as const

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

def draw_slider(screen, x, y, w, h, value, min_val, max_val, label, font):
    # рамка
    pygame.draw.rect(screen, (180, 180, 180), (x, y, w, h), 2)
    # повзунок
    knob_x = x + int((value - min_val) / (max_val - min_val) * w)
    pygame.draw.rect(screen, (200, 200, 100), (knob_x - 5, y - 5, 10, h + 10))
    # текст
    text = font.render(f"{label}: {int(value if max_val > 10 else value*100)}", True, (255, 255, 255))
    screen.blit(text, (x, y - 30))

def show_settings_screen(screen):
    cfg = load_config()
    font = pygame.font.SysFont("Arial", 28)
    small_font = pygame.font.SysFont("Arial", 24)

    apply_rect = pygame.Rect(200, 400, 150, 50)
    close_rect = pygame.Rect(400, 400, 150, 50)

    running = True
    clock = pygame.time.Clock()

    dragging = None

    while running:
        screen.fill((0, 0, 0, 180))
        pygame.draw.rect(screen, (50, 50, 50), (150, 100, 500, 300))

        # слайдери
        draw_slider(screen, 200, 180, 300, 10, cfg["volume"], 0.0, 1.0, "Volume", font)
        draw_slider(screen, 200, 280, 300, 10, cfg["fps"], 30, 240, "FPS", font)

        # кнопки
        pygame.draw.rect(screen, (100, 200, 100), apply_rect)
        pygame.draw.rect(screen, (200, 100, 100), close_rect)
        screen.blit(small_font.render("Apply", True, (0, 0, 0)), (apply_rect.x + 30, apply_rect.y + 10))
        screen.blit(small_font.render("Close", True, (0, 0, 0)), (close_rect.x + 30, close_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if apply_rect.collidepoint(event.pos):
                    save_config(cfg)
                    const.fps = cfg["fps"]
                    pygame.mixer.music.set_volume(cfg["volume"])
                    running = False
                elif close_rect.collidepoint(event.pos):
                    running = False
                elif 200 <= event.pos[0] <= 500 and 180 <= event.pos[1] <= 190:
                    dragging = "volume"
                elif 200 <= event.pos[0] <= 500 and 280 <= event.pos[1] <= 290:
                    dragging = "fps"

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = None

            elif event.type == pygame.MOUSEMOTION and dragging:
                if dragging == "volume":
                    rel = (event.pos[0] - 200) / 300
                    cfg["volume"] = max(0.0, min(1.0, rel))
                elif dragging == "fps":
                    rel = (event.pos[0] - 200) / 300
                    cfg["fps"] = int(max(30, min(240, 30 + rel * (240 - 30))))

        clock.tick(30)
