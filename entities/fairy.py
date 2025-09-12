#entities/fairy.py#

import pygame
import math
import os

class Fairy:
    def __init__(self, folder_path, player):
        #гравець до якого прив’язана фея
        self.player = player
        #завантажуємо кадри анімації
        self.frames = []
        for i in range(1, 7):
            path = os.path.join(folder_path, f"fairy_{i}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.frames.append(img)
        #параметри анімації
        self.index = 0
        self.timer = 0.0
        self.anim_speed = 0.12
        #параметри активності
        self.active = False
        self.duration = 0.0
        self.elapsed = 0.0
        #вертикальний рух для пурхання
        self.float_phase = 0.0
        #зміщення відносно гравця
        self.offset_x = 70
        self.offset_y = 40
        #напрямок сторони (для X та Y окремо)
        self.side_x = 1
        self.side_y = -1
        #збережена попередня позиція гравця
        self.prev_x, self.prev_y = self.player.rect.center

    def activate(self, duration):
        #активуємо фею на певний час
        self.active = True
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt):
        #оновлюємо анімацію та час життя
        if not self.active:
            return

        #рахуємо час активності
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.active = False
            return

        #анімація крил
        self.timer += dt
        if self.timer >= self.anim_speed:
            self.timer = 0.0
            self.index = (self.index+1) % len(self.frames)

        #ефект плавання вгору-вниз
        self.float_phase += dt*2.5

        #визначаємо напрямок руху гравця
        cx, cy = self.player.rect.center
        dx = cx - self.prev_x
        dy = cy - self.prev_y

        if abs(dx) > abs(dy):
            #рух більше по горизонталі
            if dx > 0:
                self.side_x = -1  #фея зліва
            elif dx < 0:
                self.side_x = 1   #фея справа
        elif abs(dy) > 0:
            #рух більше по вертикалі
            if dy > 0:
                self.side_y = -1  #фея зверху
            elif dy < 0:
                self.side_y = 1   #фея знизу

        #оновлюємо попередню позицію
        self.prev_x, self.prev_y = cx, cy

    def draw(self, screen):
        #малюємо фею біля гравця якщо вона активна
        if not self.active or not self.frames:
            return
        img = self.frames[self.index]
        px, py = self.player.rect.center
        px += self.side_x * self.offset_x
        py += self.side_y * self.offset_y + int(math.sin(self.float_phase)*6)
        screen.blit(img, img.get_rect(center=(px,py)))


