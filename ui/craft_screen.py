import pygame
import settings.constants as const
import os
import glob

# Глобальна змінна для зберігання анімацій зілль
potion_animations = None

def load_potion_animations():
    """Завантажує анімації для всіх типів зілль"""
    global potion_animations
    if potion_animations is not None:
        return potion_animations
        
    animations = {}
    
    # Визначаємо діапазони кадрів для кожного зілля
    potion_frames = {
        "SPEED": (0, 7),      # 0000 - 0007
        "INVISIBILITY": (0, 11), # 0000 - 0011
        "TELEPORT": (0, 7),    # 0000 - 0007
        "INVULNERABILITY": (0, 12), # 0000 - 0012
        "FLOWER_DETECTOR": (0, 13)  # 0000 - 0013
    }
    
    # Базові шляхи до папок з анімаціями
    base_path = "animations/potions"
    
    # Шляхи до папок для кожного типу зілля
    potion_paths = {
        "SPEED": os.path.join(base_path, "Small Bottle", "BLUE", "Sprites"),
        "INVISIBILITY": os.path.join(base_path, "Glowing Potion", "CYAN", "Sprite"),
        "TELEPORT": os.path.join(base_path, "Big Vial", "PURPLE", "Sprites"),
        "INVULNERABILITY": os.path.join(base_path, "Classic Jar", "BLACK_GOLD", "Sprites"),
        "FLOWER_DETECTOR": os.path.join(base_path, "Large Bottle", "GREEN", "Sprites")
    }
    
    for potion_type, path in potion_paths.items():
        frames = []
        start, end = potion_frames[potion_type]
        try:
            # Формуємо список файлів для кожного кадру
            for frame_num in range(start, end + 1):
                # Форматуємо номер кадру до 4 цифр
                frame_str = f"{frame_num:04d}"
                # Шукаємо файли, які містять номер кадру в назві
                file_pattern = os.path.join(path, f"*{frame_str}*.png")
                files = glob.glob(file_pattern)
                if files:
                    file_path = files[0]
                    img = pygame.image.load(file_path).convert_alpha()
                    # Масштабуємо до більшого розміру (наприклад, 64x64 для крафт меню)
                    img = pygame.transform.scale(img, (64, 64))
                    frames.append(img)
            
            if frames:
                animations[potion_type] = frames
            else:
                # Якщо не знайшли зображень, створюємо просту заглушку
                color = pygame.Color(const.POTION_COLORS[potion_type])
                placeholder = pygame.Surface((64, 64))
                placeholder.fill(color)
                animations[potion_type] = [placeholder]
                
        except Exception as e:
            print(f"Помилка завантаження анімації для {potion_type}: {e}")
            # Створюємо просту заглушку у випадку помилки
            color = pygame.Color(const.POTION_COLORS[potion_type])
            placeholder = pygame.Surface((64, 64))
            placeholder.fill(color)
            animations[potion_type] = [placeholder]
    
    potion_animations = animations
    return animations

def show_craft_menu(game):
    potions = [
        {"name": "Speed Potion", "cost": const.POTION_COSTS["SPEED"], "effect": "SPEED", "key": "1"},
        {"name": "Invisibility Potion", "cost": const.POTION_COSTS["INVISIBILITY"], "effect": "INVISIBILITY", "key": "2"},
        {"name": "Teleport Potion", "cost": const.POTION_COSTS["TELEPORT"], "effect": "TELEPORT", "key": "3"},
        {"name": "Invulnerability Potion", "cost": const.POTION_COSTS["INVULNERABILITY"], "effect": "INVULNERABILITY", "key": "4"},
        {"name": "Flower Detector Potion", "cost": const.POTION_COSTS["FLOWER_DETECTOR"], "effect": "FLOWER_DETECTOR", "key": "5"}
    ]
    
    # Завантажуємо анімації зілль
    potion_animations = load_potion_animations()
    animation_timer = 0
    animation_speed = 0.1
    current_frame = 0
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        dt = clock.tick(const.fps) / 1000.0
        
        # Оновлюємо анімацію
        animation_timer += dt
        if animation_timer >= animation_speed:
            animation_timer = 0
            current_frame = (current_frame + 1) % 20  # 20 кадрів для плавнішої анімації
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_1:
                    craft_potion(game, "SPEED")
                elif event.key == pygame.K_2:
                    craft_potion(game, "INVISIBILITY")
                elif event.key == pygame.K_3:
                    craft_potion(game, "TELEPORT")
                elif event.key == pygame.K_4:
                    craft_potion(game, "INVULNERABILITY")
                elif event.key == pygame.K_5:
                    craft_potion(game, "FLOWER_DETECTOR")
        
        # малюємо меню крафтингу
        game.screen.fill((30, 30, 40))
        font_title = pygame.font.SysFont(None, 48)
        font_item = pygame.font.SysFont(None, 32)
        font_small = pygame.font.SysFont(None, 24)
        
        # заголовок
        title = font_title.render("Crafting Menu", True, const.colors["WHITE"])
        game.screen.blit(title, (game.screen.get_width()//2 - title.get_width()//2, 50))
        
        # інформація про квіти
        flowers_text = font_item.render(f"Flowers: {game.player.flowers}", True, const.colors["YELLOW"])
        game.screen.blit(flowers_text, (game.screen.get_width()//2 - flowers_text.get_width()//2, 120))
        
        # список зіллів
        for i, potion in enumerate(potions):
            y_pos = 180 + i * 90  # Збільшуємо відстань між рядками
            color = const.colors["GREEN"] if game.player.flowers >= potion["cost"] else const.colors["RED"]
            
            # Відображаємо анімоване зілля
            if potion["effect"] in potion_animations:
                frames = potion_animations[potion["effect"]]
                frame_index = current_frame % len(frames)
                potion_image = frames[frame_index]
                game.screen.blit(potion_image, (game.screen.get_width()//2 - 400, y_pos))
            
            # назва та вартість
            text = font_item.render(f"{potion['key']}. {potion['name']} - {potion['cost']} flowers", True, color)
            game.screen.blit(text, (game.screen.get_width()//2 - 120, y_pos + 15))
            
            # опис
            desc_text = font_small.render(f"Effect: {get_potion_description(potion['effect'])}", True, const.colors["WHITE"])
            game.screen.blit(desc_text, (game.screen.get_width()//2 - desc_text.get_width()//2, y_pos + 45))
        
        # інструкція
        instruction = font_small.render("Press ESC to return to game", True, const.colors["GRAY"])
        game.screen.blit(instruction, (game.screen.get_width()//2 - instruction.get_width()//2, game.screen.get_height() - 50))
        
        pygame.display.flip()
    
    return True

def get_potion_description(effect):
    # опис ефектів зіллів
    descriptions = {
        "SPEED": "Increases movement speed for 5 seconds",
        "INVISIBILITY": "Makes you invisible and prevents NPC interaction for 7 seconds",
        "TELEPORT": "Teleports you to a random safe location",
        "INVULNERABILITY": "Makes you invulnerable to all damage for 10 seconds",
        "FLOWER_DETECTOR": "Automatically collects all flowers in the room and lasts for 2 minutes"
    }
    return descriptions.get(effect, "Unknown effect")

def craft_potion(game, potion_type):
    # перевіряємо чи достатньо квітів
    cost = const.POTION_COSTS[potion_type]
    if game.player.flowers >= cost:
        game.player.flowers -= cost
        game.player.potion_inventory.inventory[potion_type] += 1
        return True
    return False