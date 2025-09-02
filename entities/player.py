import pygame
from entities.animation_manager import AnimationManager
import settings.constants as const
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, start_sector=(0,0)):
        super().__init__()
        self.sector = start_sector
        self.base_speed = 4
        self.speed = self.base_speed

        # ініціалізація менеджера анімацій
        self.anim = AnimationManager("animations/goblin")

        # початкові координати (використовуємо const.tile_px)
        w, h = const.tile_px, const.tile_px
        spawn_x = const.tile_px + const.tile_px//2 - w//2
        spawn_y = const.tile_px + const.tile_px//2 - h//2
        self.rect = pygame.Rect(spawn_x, spawn_y, w, h)

        self.state = 'idle'
        self.direction = 'down'

        # --- Лічильник зібраних квітів ---
        self.flowers = 0

        # --- Баф швидкості ---
        self.boost_active = False
        self.boost_end_time = 0

    def get_sector(self):
        return self.sector

    def activate_speed_boost(self):
        """Активація бафа швидкості, якщо є 3 квітки"""
        if self.flowers >= 3 and not self.boost_active:
            self.flowers -= 3
            self.speed = self.base_speed * 2.5
            self.boost_active = True
            self.boost_end_time = time.time() + 7  # тривалість 7 секунд
            return True
        return False

    def update(self, dt, walls):
        # --- Перевірка чи не закінчився баф ---
        if self.boost_active and time.time() >= self.boost_end_time:
            self.speed = self.base_speed
            self.boost_active = False

        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_a]: dx = -self.speed; self.direction = 'left'
        elif keys[pygame.K_d]: dx = self.speed; self.direction = 'right'
        if keys[pygame.K_w]: dy = -self.speed; self.direction = 'up'
        elif keys[pygame.K_s]: dy = self.speed; self.direction = 'down'

        # рух + колізії
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0: self.rect.right = wall.left
                if dx < 0: self.rect.left = wall.right

        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0: self.rect.bottom = wall.top
                if dy < 0: self.rect.top = wall.bottom

        # визначення стану
        self.state = 'idle' if dx == 0 and dy == 0 else 'walk'

        # оновлення анімації
        self.anim.update(dt, self.state, self.direction)

    def draw(self, screen):
        screen.blit(self.anim.get_image(), self.rect)
