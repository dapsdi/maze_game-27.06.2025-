#entities/potion_inventory.py#
import pygame
import time
import random
import settings.constants as const
import os
import glob

class PotionInventory:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.inventory = {
            "SPEED": 0,
            "INVISIBILITY": 0,
            "TELEPORT": 0,
            "INVULNERABILITY": 0, 
            "FLOWER_DETECTOR": 0
        }
        self.active_effects = {}
        self.visible = True
        self.invulnerable = False
        self.flower_detector_active = False
        
        # Завантажуємо анімації зілль
        self.potion_animations = self.load_potion_animations()
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # секунди між кадрами

    def load_potion_animations(self):
        """Завантажує анімації для всіх типів зілль"""
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
                        # Масштабуємо до більшого розміру (наприклад, 48x48)
                        img = pygame.transform.scale(img, (40, 60))
                        frames.append(img)
                
                if frames:
                    animations[potion_type] = frames
                else:
                    # Якщо не знайшли зображень, створюємо просту заглушку
                    color = pygame.Color(const.POTION_COLORS[potion_type])
                    placeholder = pygame.Surface((48, 48))
                    placeholder.fill(color)
                    animations[potion_type] = [placeholder]
                    
            except Exception as e:
                print(f"Помилка завантаження анімації для {potion_type}: {e}")
                # Створюємо просту заглушку у випадку помилки
                color = pygame.Color(const.POTION_COLORS[potion_type])
                placeholder = pygame.Surface((48, 48))
                placeholder.fill(color)
                animations[potion_type] = [placeholder]
        
        return animations

    def update_effects(self, dt):
        current_time = time.time()
        effects_to_remove = []
        
        for effect, end_time in self.active_effects.items():
            if current_time >= end_time:
                effects_to_remove.append(effect)

        for effect in effects_to_remove:
            self.deactivate_effect(effect)
            
        # Оновлюємо анімацію
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 10  # 10 кадрів для всіх анімацій

    def use_potion(self, potion_type):
        if self.inventory[potion_type] > 0:
            self.inventory[potion_type] -= 1
            self.activate_effect(potion_type)
            return True
        return False

    def activate_effect(self, potion_type):
        if potion_type == "SPEED":
            self.player.speed = self.player.base_speed * 2.5
            self.active_effects["SPEED"] = time.time() + const.POTION_DURATIONS["SPEED"] / 1000.0
        
        elif potion_type == "INVISIBILITY":
            self.visible = False
            self.active_effects["INVISIBILITY"] = time.time() + const.POTION_DURATIONS["INVISIBILITY"] / 1000.0
        
        elif potion_type == "TELEPORT":
            self.teleport_player()
        
        elif potion_type == "INVULNERABILITY":  # змінили
            self.invulnerable = True
            self.active_effects["INVULNERABILITY"] = time.time() + const.POTION_DURATIONS["INVULNERABILITY"] / 1000.0
        
        elif potion_type == "FLOWER_DETECTOR":
            self.flower_detector_active = True
            self.active_effects["FLOWER_DETECTOR"] = time.time() + const.POTION_DURATIONS["FLOWER_DETECTOR"] / 1000.0
            # автоматично збираємо квіти в поточному секторі
            self.collect_flowers_in_sector()

    def deactivate_effect(self, effect_type):
        if effect_type == "SPEED":
            self.player.speed = self.player.base_speed
        elif effect_type == "INVISIBILITY":
            self.visible = True
        elif effect_type == "INVULNERABILITY":
            self.invulnerable = False
        elif effect_type == "FLOWER_DETECTOR":
            self.flower_detector_active = False

        if effect_type in self.active_effects:
            del self.active_effects[effect_type]

    def collect_flowers_in_sector(self):
        # збираємо всі квіти в поточному секторі
        sector = self.player.get_sector()
        chests = self.game.map_controller.get_chests(sector)
        if chests:
            # симулюємо збір квітів
            collected = len(chests)
            self.player.flowers += collected
            # очищаємо список квітів у секторі
            self.game.map_controller.grid[sector[0]][sector[1]]['chests'] = []
            
    def teleport_player(self):
        # телепортуємо гравця в випадкову позицію
        sector = self.player.get_sector()
        walls = self.game.map_controller.get_walls(sector)
        
        # знаходимо випадкову позицію, де немає стін
        while True:
            x = random.randint(50, const.sector_size - 50)
            y = random.randint(50, const.sector_size - 50)
            temp_rect = pygame.Rect(x - 25, y - 25, 50, 50)
            
            collision = False
            for wall in walls:
                if temp_rect.colliderect(wall.rect):
                    collision = True
                    break
                    
            if not collision:
                self.player.rect.center = (x, y)
                break

    def draw(self, screen):
        if not self.visible:
            return
            
        # малюємо інвентар зіллів
        font = pygame.font.SysFont(None, 24)
        x, y = 20, screen.get_height() - 340  # Зміщуємо вище, щоб було більше місця
        
        for i, (potion_type, count) in enumerate(self.inventory.items()):
            # Отримуємо поточний кадр анімації для цього зілля
            if potion_type in self.potion_animations:
                frames = self.potion_animations[potion_type]
                frame_index = self.current_frame % len(frames)
                potion_image = frames[frame_index]
                
                # Малюємо зображення зілля (розмір 48x48)
                screen.blit(potion_image, (x, y + i * 70))  # Збільшуємо відстань між рядками
                # Малюємо текст з кількістю
                text = font.render(f"{count}", True, (255, 255, 255))
                screen.blit(text, (x + 50, y + i * 60 + 15))  # Зміщуємо текст праворуч від зображення