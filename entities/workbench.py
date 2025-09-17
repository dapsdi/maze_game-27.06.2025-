# workbench.py #

import pygame
import os
import random

class Workbench:
    def __init__(self, pos):
        # Завантажуємо кадри анімації
        self.frames = []
        frames_dir = "animations/crafting_table"
        
        # Завантажуємо всі кадри анімації
        for i in range(1, 4):  # файли crafting_table_1.png до crafting_table_3.png
            frame_path = os.path.join(frames_dir, f"crafting_table_{i}.png")
            try:
                if os.path.exists(frame_path):
                    frame = pygame.image.load(frame_path).convert_alpha()
                    self.frames.append(frame)
                else:
                    print(f"Попередження: Не вдалося знайти файл {frame_path}")
            except Exception as e:
                print(f"Помилка завантаження {frame_path}: {e}")
        
        # Якщо не знайшли жодного кадру, створюємо простий квадрат як заглушку
        if not self.frames:
            self.frames = [pygame.Surface((50, 50))]
            self.frames[0].fill((139, 69, 19))  # коричневий
        
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=pos)
        
        # Налаштування анімації
        self.animation_timer = 0
        self.animation_speed = 0.2  # секунди між кадрами

    def update(self, dt):
        # Оновлюємо анімацію
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect)