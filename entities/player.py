import pygame
from entities.animation_manager import AnimationManager
from entities.potion_inventory import PotionInventory
import settings.constants as const
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, start_sector=(0,0), game=None):
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
        self.noclip = False  #режим без колізій
        
        #шлях до анімацій гравця
        self.animation_manager = AnimationManager("animations/goblin")
        self.image = self.animation_manager.get_image()
        self.rect = self.image.get_rect()
        self.rect.center = (const.sector_size // 2, const.sector_size // 2)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  #час між кадрами анімації
        self.state = 'idle'  #стан гравця для анімації
        
        #інвентар зіллів
        self.potion_inventory = PotionInventory(self, self.game)

    def update(self, dt, walls):
        #зберігаємо стару позицію для відкату при колізії
        old_x, old_y = self.rect.x, self.rect.y
        
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        #прапор руху
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
            
        #визначаємо стан (рух чи спокій)
        self.state = 'walk' if moving else 'idle'
        
        #якщо режим noclip увімкнений, рухаємося без колізій
        if self.noclip:
            self.rect.x += dx
            self.rect.y += dy
        else:
            #рухаємося по осі X і перевіряємо колізії
            self.rect.x += dx
            for wall in walls:
                if self.rect.colliderect(wall):
                    if dx > 0:  #рух праворуч
                        self.rect.right = wall.left
                    elif dx < 0:  #рух ліворуч
                        self.rect.left = wall.right
                    break
                    
            #рухаємося по осі Y і перевіряємо колізії
            self.rect.y += dy
            for wall in walls:
                if self.rect.colliderect(wall):
                    if dy > 0:  #рух униз
                        self.rect.bottom = wall.top
                    elif dy < 0:  #рух вгору
                        self.rect.top = wall.bottom
                    break
                    
        #оновлюємо анімацію
        self.animation_manager.update(dt, self.state, self.direction)
        self.image = self.animation_manager.get_image()
            
        #оновлюємо невразливість
        if self.invincible:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.invincible = False
                
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