#map.py#
import pygame
import random
from settings import *

class Map:
    def __init__(self):
        #створюємо список з рядками по map_width і в кожному рядку стільки словників, скільки map_height
        #кожен словник має ключі visited(чи відвідували цей сектор) і walls(які стіни є в секторі)
        #в walls зберігаються True там, де є стіна, спочатку усі стіни закриті(всі True)
        self.sectors = [[{
            'visited': False,
            'walls': {"top": True, "bottom": True, "left": True, "right": True}
        } for _ in range(map_height)] for _ in range(map_width)]

        #створюємо випадкову позицію скарбу в межах карти, це кортеж з двох чисел
        self.treasure_position = (random.randint(0, map_width - 1), random.randint(0, map_height - 1))

        #відразу запускаємо створення лабіринту на карті
        self.generate_maze()

    def generate_maze(self):
        #створюємо пустий список, який буде пам'ятати шлях назад
        stack = []
                                             #total_cells - загальна кількість секторів на карті
        total_cells = map_width * map_height #запам'ятовуємо скільки всього секторів на карті (потрібно, щоб знати коли закінчити)
        
        #лічильник уже відвіданих секторів під час побудови, починається з 1 бо ми у першому секторі з'явилися
        visited_cells = 1

        #вибираємо випадковий сектор, з якого почнемо будувати лабіринт
        #current_cell - кортеж(кортеж це незмінюваний список) з початковими координатами
        current_cell = (random.randint(0, map_width - 1), random.randint(0, map_height - 1))
        
        #позначаємо цей сектор як відвіданий
        self.sectors[current_cell[0]][current_cell[1]]['visited'] = True

        #поки ми не відвідали всі сектори, виконуємо наступне
        while visited_cells < total_cells:
            #знаходимо всі сусідні сектори, які ще не були відвідані
            neighbors = self.get_unvisited_neighbors(current_cell)

            if neighbors:
                #якщо є такі сусіди, вибираємо одного випадково
                next_cell = random.choice(neighbors)

                #видаляємо стіни між поточним і обраним сусіднім сектором
                self.remove_wall(current_cell, next_cell)

                #запам'ятовуємо поточний сектор, щоб потім повернутися назад
                stack.append(current_cell)
                #переходимо до обраного сусіднього сектора
                current_cell = next_cell
                #позначаємо цей новий сектор як відвіданий
                self.sectors[current_cell[0]][current_cell[1]]['visited'] = True
                #збільшуємо лічильник відвіданих секторів
                visited_cells += 1
            elif stack:
                #якщо немає не відвіданих сусідів, повертаємося до останнього сектору зі шляху назад
                current_cell = stack.pop()
            else:
                #якщо стек порожній, але не всі сектори відвідані (дуже рідко)
                #знаходимо всі сектори, які не відвідували раніше
                unvisited_cells = [(x, y) for x in range(map_width) for y in range(map_height) if not self.sectors[x][y]['visited']]
                if unvisited_cells:
                    #вибираємо випадковий невідвіданий сектор
                    current_cell = random.choice(unvisited_cells)
                    #позначаємо його як відвіданий
                    self.sectors[current_cell[0]][current_cell[1]]['visited'] = True
                    #збільшуємо лічильник
                    visited_cells += 1
                    #додаємо цей сектор у стек, щоб пам'ятати шлях назад
                    stack.append(current_cell)
        
    def get_unvisited_neighbors(self, cell):
        #отримуємо x і y позиції сектора
        x, y = cell
        #створюємо пустий список для сусідів
        neighbors = []
        #перевіряємо чи можна піти вліво і чи там ще не відвідували
        if x > 0 and not self.sectors[x-1][y]['visited']:
            neighbors.append((x-1, y))
        #перевіряємо чи можна піти вправо і чи там ще не відвідували
        if x < map_width -1 and not self.sectors[x+1][y]['visited']:
            neighbors.append((x+1, y))
        #перевіряємо чи можна піти вгору і чи там ще не відвідували
        if y > 0 and not self.sectors[x][y-1]['visited']:
            neighbors.append((x, y-1))
        #перевіряємо чи можна піти вниз і чи там ще не відвідували
        if y < map_height -1 and not self.sectors[x][y+1]['visited']:
            neighbors.append((x, y+1))
        #повертаємо список всіх не відвіданих сусідів
        return neighbors
    
    def remove_wall(self, current, next_):
        #отримуємо x,y поточного і наступного секторів
        cx, cy = current
        nx, ny = next_

        #якщо наступний сектор праворуч
        if nx == cx + 1:
            #прибираємо праву стіну у поточного сектору
            self.sectors[cx][cy]['walls']['right'] = False
            #прибираємо ліву стіну у наступного сектору
            self.sectors[nx][ny]['walls']['left'] = False
        #якщо наступний сектор ліворуч
        elif nx == cx - 1:
            #прибираємо ліву стіну у поточного сектору
            self.sectors[cx][cy]['walls']['left'] = False
            #прибираємо праву стіну у наступного сектору
            self.sectors[nx][ny]['walls']['right'] = False
        #якщо наступний сектор знизу
        elif ny == cy + 1:
            #прибираємо нижню стіну у поточного сектору
            self.sectors[cx][cy]['walls']['bottom'] = False
            #прибираємо верхню стіну у наступного сектору
            self.sectors[nx][ny]['walls']['top'] = False
        #якщо наступний сектор зверху
        elif ny == cy - 1:
            #прибираємо верхню стіну у поточного сектору
            self.sectors[cx][cy]['walls']['top'] = False
            #прибираємо нижню стіну у наступного сектору
            self.sectors[nx][ny]['walls']['bottom'] = False
    
    def draw_current_sector(self, screen, player_sector):
        #отримуємо координати сектора гравця (x,y)
        px, py = player_sector
        #малюємо фон сектора жовтим кольором, з початку координат (0,0), розміром sector_size на sector_size
        pygame.draw.rect(screen, colors["YELLOW"], (0, 0, sector_size, sector_size))

        #беремо інформацію про стіни поточного сектора
        walls = self.sectors[px][py]['walls']
        #визначаємо товщину стінки
        thickness = 5
        #якщо верхня стіна є, малюємо її сірим кольором вгорі сектора
        if walls['top']:
            pygame.draw.rect(screen, colors["GRAY"], (0, 0, sector_size, thickness))
        #якщо нижня стіна є, малюємо її внизу сектора
        if walls['bottom']:
            pygame.draw.rect(screen, colors["GRAY"], (0, sector_size - thickness, sector_size, thickness))
        #якщо ліва стіна є, малюємо її зліва
        if walls['left']:
            pygame.draw.rect(screen, colors["GRAY"], (0, 0, thickness, sector_size))
        #якщо права стіна є, малюємо її справа
        if walls['right']:
            pygame.draw.rect(screen, colors["GRAY"], (sector_size - thickness, 0, thickness, sector_size))

        #якщо гравець у секторі зі скарбом
        if (px, py) == self.treasure_position:
            #малюємо скарб у вигляді зеленого кола в центрі сектора
            pygame.draw.circle(screen, colors["GREEN"], (sector_size // 2, sector_size // 2), 20)

    def get_walls(self, player_sector):
        #створюємо порожній список для стін у вигляді прямокутників pygame.Rect
        walls_rects = []
        #отримуємо координати поточного сектора
        px, py = player_sector
        #беремо дані про стіни цього сектора
        sector = self.sectors[px][py]
        #товщина стіни в пікселях
        thickness = 5
        #якщо є верхня стіна, додаємо прямокутник у список стін
        if sector['walls']['top']:
            walls_rects.append(pygame.Rect(0, 0, sector_size, thickness))
        #якщо є нижня стіна, додаємо прямокутник у список
        if sector['walls']['bottom']:
            walls_rects.append(pygame.Rect(0, sector_size - thickness, sector_size, thickness))
        #якщо є ліва стіна, додаємо прямокутник у список
        if sector['walls']['left']:
            walls_rects.append(pygame.Rect(0, 0, thickness, sector_size))
        #якщо є права стіна, додаємо прямокутник у список
        if sector['walls']['right']:
            walls_rects.append(pygame.Rect(sector_size - thickness, 0, thickness, sector_size))
        #повертаємо список всіх стін для колізій та малювання
        return walls_rects
