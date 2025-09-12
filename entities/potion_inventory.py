import pygame
import time
import random
import settings.constants as const

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
        self.invulnerable = False  # новий ефект
        self.flower_detector_active = False

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

    def update_effects(self, dt):
        current_time = time.time()
        effects_to_remove = []
        
        for effect, end_time in self.active_effects.items():
            if current_time >= end_time:
                effects_to_remove.append(effect)

        for effect in effects_to_remove:
            self.deactivate_effect(effect)

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
        x, y = 20, screen.get_height() - 150
        
        for i, (potion_type, count) in enumerate(self.inventory.items()):
            color_name = const.POTION_COLORS.get(potion_type, "#FFFFFF")
            color = pygame.Color(color_name)
            
            # малюємо прямокутник з кольором зілля
            pygame.draw.rect(screen, color, (x, y + i * 30, 20, 20))
            # малюємо текст з кількістю
            text = font.render(f"{potion_type}: {count}", True, (255, 255, 255))
            screen.blit(text, (x + 30, y + i * 30))