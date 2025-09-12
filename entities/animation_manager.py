#entities/animation_manager.py
import os
import pygame
import settings.constants as const

class AnimationManager:
    def __init__(self, base_path, animation_speed=0.1):
        self.base_path = base_path
        self.animation_speed = animation_speed

        # Всі анімації зберігаються у словнику self.animations[стан][напрямок]
        self.animations = {}
        self.load_animations()

        # Початкові параметри анімації
        self.state = 'idle'
        self.direction = 'down'
        self.frame_index = 0
        self.timer = 0

        # Поточне зображення
        self.image = self.animations[self.state][self.direction][0]

    def load_animations(self):
        # Завантаження анімацій з файлової системи
        states = ['idle', 'walk']
        
        for state in states:
            self.animations[state] = {}
            
            for direction in ['down', 'left', 'right', 'up']:
                # Формуємо шлях до папки з анімаціями
                if state == 'idle':
                    dir_path = os.path.join(self.base_path, 'idle', f'idle_{direction}')
                else:  # walk
                    dir_path = os.path.join(self.base_path, 'walk', f'walk_{direction}')
                
                frames = []
                
                if os.path.exists(dir_path):
                    # Отримуємо список файлів і сортуємо їх за назвою
                    files = sorted([f for f in os.listdir(dir_path) if f.endswith('.gif')])
                    for fname in files:
                        full_path = os.path.join(dir_path, fname)
                        img = pygame.image.load(full_path).convert_alpha()
                        img = pygame.transform.scale(img, (const.tile_px, const.tile_px))
                        frames.append(img)
                else:
                    # Створюємо заглушку, якщо папка не знайдена
                    print(f"Warning: Animation directory not found: {dir_path}")
                    frames = [self.create_placeholder_image((100, 100, 100))]
                
                self.animations[state][direction] = frames

    def create_placeholder_image(self, color):
        # Створюємо просте зображення-заглушку
        image = pygame.Surface((const.tile_px, const.tile_px))
        image.fill(color)
        pygame.draw.rect(image, (0, 0, 0), (0, 0, const.tile_px, const.tile_px), 1)
        return image

    def update(self, dt, state, direction):
        # Оновлення стану і напрямку
        if state != self.state or direction != self.direction:
            self.state = state
            self.direction = direction
            self.frame_index = 0
            self.timer = 0

        # Оновлення таймера і кадру
        self.timer += dt
        if self.timer >= self.animation_speed:
            self.timer -= self.animation_speed
            frames = self.animations[self.state][self.direction]
            if frames:  # Якщо є кадри
                self.frame_index = (self.frame_index + 1) % len(frames)
            else:
                self.frame_index = 0
        
        # Оновлення зображення
        if self.animations[self.state][self.direction]:
            self.image = self.animations[self.state][self.direction][self.frame_index]
        else:
            # Якщо немає кадрів, використовуємо заглушку
            self.image = self.create_placeholder_image((255, 0, 0))

    def get_image(self):
        return self.image