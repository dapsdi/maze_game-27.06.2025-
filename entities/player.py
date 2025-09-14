import pygame
from entities.animation_manager import AnimationManager
from entities.potion_inventory import PotionInventory
import settings.constants as const
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, start_sector=(0,0), game=None, pos=None):
        super().__init__()
        self.game = game
        self.sector_x, self.sector_y = start_sector
        self.base_speed = const.PLAYER_SPEED
        self.speed = self.base_speed
        self.health = const.PLAYER_MAX_HEALTH
        self.max_health = const.PLAYER_MAX_HEALTH
        self.flowers = 300
        self.direction = "down"
        self.invincible = False
        self.invincibility_timer = 0
        self.noclip = False
        
        # Додаємо акумулятори для точного руху
        self.x_accumulator = 0.0
        self.y_accumulator = 0.0
        
        # Зменшуємо розмір гравця для кращого проходження через двері
        self.hitbox_width = 50
        self.hitbox_height = 50
        
        self.animation_manager = AnimationManager("animations/goblin")
        self.image = self.animation_manager.get_image()
        self.rect = self.image.get_rect()
        
        # Використовуємо передану позицію або центр сектора
        if pos:
            self.rect.center = pos
            self.x, self.y = pos
        else:
            center_x = const.sector_size // 2
            center_y = const.sector_size // 2
            self.rect.center = (center_x, center_y)
            self.x, self.y = center_x, center_y
            
        # Створюємо окремий хітбокс для колізій
        self.hitbox = pygame.Rect(0, 0, self.hitbox_width, self.hitbox_height)
        self.hitbox.center = self.rect.center
            
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.state = 'idle'
        
        self.potion_inventory = PotionInventory(self, self.game)

    def update(self, dt, walls):
        # Зберігаємо стару позицію для відкату при колізії
        old_x, old_y = self.x, self.y
        
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        moving = False
        
        if keys[pygame.K_w]:
            dy = -self.speed * dt
            self.direction = "up"
            moving = True
        if keys[pygame.K_s]:
            dy = self.speed * dt
            self.direction = "down"
            moving = True
        if keys[pygame.K_a]:
            dx = -self.speed * dt
            self.direction = "left"
            moving = True
        if keys[pygame.K_d]:
            dx = self.speed * dt
            self.direction = "right"
            moving = True
            
        self.state = 'walk' if moving else 'idle'
        
        # Додаємо рух до акумуляторів
        self.x_accumulator += dx
        self.y_accumulator += dy
        
        # Отримуємо цілу частину руху
        move_x = int(self.x_accumulator)
        move_y = int(self.y_accumulator)
        
        # Зберігаємо дробову частину для наступного кадру
        self.x_accumulator -= move_x
        self.y_accumulator -= move_y
        
        if self.noclip:
            self.x += move_x
            self.y += move_y
        else:
            # Рухаємо спочатку по X
            self.x += move_x
            self.hitbox.center = (int(self.x), int(self.y))
            collision = self.check_collisions(walls)
            if collision:
                self.x = old_x
                self.x_accumulator = 0.0  # Скидаємо акумулятор при колізії
                
            # Потім по Y
            self.y += move_y
            self.hitbox.center = (int(self.x), int(self.y))
            collision = self.check_collisions(walls)
            if collision:
                self.y = old_y
                self.y_accumulator = 0.0  # Скидаємо акумулятор при колізії
                
        # Оновлюємо позицію rect на основі float координат
        self.rect.center = (int(self.x), int(self.y))
        self.hitbox.center = self.rect.center
            
        # Оновлюємо анімацію
        self.animation_manager.update(dt, self.state, self.direction)
        self.image = self.animation_manager.get_image()
            
        if self.invincible:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.invincible = False
                
    def check_collisions(self, walls):
        for wall in walls:
            if self.hitbox.colliderect(wall):
                return True
        return False

    def take_damage(self, amount):
        #перевіряємо чи не є гравець невразливим (через зілля)
        if self.potion_inventory.invulnerable:
            return False
            
        if self.invincible:
            return False
            
        self.health -= amount
        self.invincible = True
        self.invincibility_timer = const.INVINCIBILITY_DURATION
        
        if self.health <= 0:
            self.die()
            return True
        return False

    def die(self):
        #обробка смерті гравця
        self.health = 0
        self.game.game_over = True

    def get_sector(self):
        return (self.sector_x, self.sector_y)

    def set_sector(self, x, y):
        self.sector_x = x
        self.sector_y = y

    def draw(self, screen):
        #малюємо гравця на екрані
        screen.blit(self.image, self.rect)