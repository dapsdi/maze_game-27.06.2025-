import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="basic"):
        super().__init__()
        self.x = x
        self.y = y
        self.type = enemy_type
        
        #базові характеристики
        self.speed = 2.0
        self.damage = 10
        self.health = 50
        self.attack_range = 50
        self.attack_cooldown = 1.0
        self.last_attack = 0
        
        #створюємо простий спрайт
        self.image = pygame.Surface((32, 32))
        if enemy_type == "basic":
            self.image.fill((255, 0, 0))  #червоний для базового ворога
        elif enemy_type == "ranged":
            self.image.fill((0, 0, 255))  #синій для дальнього ворога
            self.attack_range = 150
        else:
            self.image.fill((128, 128, 128))  #сірий для інших типів
            
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, dt, player, walls):
        #рухаємося до гравця
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(0.1, math.sqrt(dx*dx + dy*dy))
        
        #нормалізуємо напрямок
        dx /= dist
        dy /= dist
        
        #рухаємо ворога
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        #перевіряємо колізії зі стінами
        for wall in walls:
            if self.rect.colliderect(wall):
                #відступаємо від стіни
                if dx > 0: self.rect.right = wall.left
                elif dx < 0: self.rect.left = wall.right
                if dy > 0: self.rect.bottom = wall.top
                elif dy < 0: self.rect.top = wall.bottom
        
        #перевіряємо атаку
        self.last_attack += dt
        if dist < self.attack_range and self.last_attack >= self.attack_cooldown:
            self.attack(player)
            self.last_attack = 0

    def attack(self, player):
        #атакуємо гравця
        player.take_damage(self.damage)

    def take_damage(self, amount):
        #отримуємо шкоду
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        #смерть ворога
        self.kill()