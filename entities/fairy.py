import pygame
import os

class Fairy(pygame.sprite.Sprite):
    def __init__(self, folder, player):
        super().__init__()
        self.frames = []
        for i in range(1, 8):  # fairy_1.png ... fairy_7.png
            path = os.path.join(folder, f"fairy_{i}.png")
            img = pygame.image.load(path).convert_alpha()
            self.frames.append(img)

        self.player = player
        self.active = False
        self.timer = 0
        self.frame_index = 0
        self.frame_speed = 0.12  # швидкість анімації

        # позиція феї
        self.offset = (-90, -60)  # відносно гравця (можна підкрутити)

        #параметри літання

    def activate(self, duration):
        """Запускає фею на duration секунд"""
        self.active = True
        self.timer = duration
        self.frame_index = 0

    def update(self, dt):
        if not self.active:
            return

        # таймер часу життя
        self.timer -= dt
        if self.timer <= 0:
            self.active = False
            return

        # оновлення кадрів анімації
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

    def draw(self, screen):
        if not self.active:
            return
        print("Fairy drawing frame:", int(self.frame_index))  # ← дебаг
        img = self.frames[int(self.frame_index)]
        x = self.player.rect.centerx + self.offset[0]
        y = self.player.rect.centery + self.offset[1]
        screen.blit(img, (x, y))
