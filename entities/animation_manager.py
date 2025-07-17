#entities/animation_manager.py
import os
import pygame
import settings.constants as const

class AnimationManager:
    def __init__(self, base_path, animation_speed=0.1):
        #base_path — шлях до папки зі спрайтами
        self.base_path = base_path
        self.animation_speed = animation_speed

        #всі анімації зберігаються у словнику self.animations[стан][напрямок]
        self.animations = {}
        self.load_animations()

        #початкові параметри анімації
        self.state = 'idle'
        self.direction = 'down'
        self.frame_index = 0
        self.timer = 0

        #поточне зображення
        self.image = self.animations[self.state][self.direction][0]

    def load_animations(self):
        #завантаження анімацій з файлової системи
        for state in ('idle', 'walk'):
            self.animations[state] = {}
            state_dir = os.path.join(self.base_path, state)
            for direction in ('up', 'down', 'left', 'right'):
                dir_path = os.path.join(state_dir, f"{state}_{direction}")
                frames = []
                if not os.path.exists(dir_path): continue
                for fname in sorted(os.listdir(dir_path)):
                    if fname.endswith(".gif"):
                        full_path = os.path.join(dir_path, fname)
                        img = pygame.image.load(full_path).convert_alpha()
                        img = pygame.transform.scale(img, (const.tile_px, const.tile_px))
                        frames.append(img)
                self.animations[state][direction] = frames

    def update(self, dt, state, direction):
        #оновлення стану і напрямку
        if state != self.state or direction != self.direction:
            self.state = state
            self.direction = direction
            self.frame_index = 0
            self.timer = 0

        #оновлення таймера і кадру
        self.timer += dt
        if self.timer >= self.animation_speed:
            self.timer -= self.animation_speed
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.state][self.direction])
        
        #оновлення зображення
        self.image = self.animations[self.state][self.direction][self.frame_index]

    def get_image(self):
        return self.image
