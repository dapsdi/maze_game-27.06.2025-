# map/map_controller.py
import pygame
import random
import settings.constants as const #імпортуємо константи з модуля settings.constants
from ui.colors import colors

class MapController:
    def __init__(self):
        #створюємо двовимірний список grid, де кожен елемент — це словник з даними про сектор; const.map_width і const.map_height визначають розміри лабіринту
        self.grid = [
            [
                {
                    'visited': False, #означає, чи був сектор відвіданий при генерації глобального лабіринту; використовується у generate_full_maze
                    'walls': {'top': True, 'bottom': True, 'left': True, 'right': True}, #словник, який зберігає наявність стін сектора; всі стіни спочатку присутні
                    'tiles': self.generate_tile_maze(), #двовимірний масив, що описує локальний лабіринт у секторі; генерується функцією generate_tile_maze
                    'chests': [], #список сундуків у секторі; заповнюється після генерації проходів
                    'entry_points': [] #список точок входу у сектор; заповнюється після видалення стін
                }
                for _ in range(const.map_height)
            ]
            for _ in range(const.map_width)
        ]
        #генеруємо випадкову позицію фінального скарбу; random.randrange(const.map_width) та random.randrange(const.map_height) вибирають координати у межах лабіринту
        self.treasure_pos = (
            random.randrange(const.map_width),
            random.randrange(const.map_height)
        )
        #генеруємо глобальний лабіринт між секторами; видаляємо стіни для створення проходів
        self.generate_full_maze()

        #додаємо точки входу та сундуки у кожен сектор після того, як визначені проходи між секторами
        for x in range(const.map_width):
            for y in range(const.map_height):
                entries = [] #тимчасовий список для точок входу у сектор
                for direction, is_wall in self.grid[x][y]['walls'].items(): #перебираємо всі напрямки стін
                    if not is_wall: #якщо стіна відсутня, створюємо точку входу
                        offset = random.randint(const.entry_offset_min, const.entry_offset_max) #offset визначає зсув отвору на краю сектора
                        entries.append((direction, offset)) #додаємо точку входу у список
                        self.apply_entry_point(self.grid[x][y]['tiles'], direction, offset) #вирізаємо отвір у локальному лабіринті
                self.grid[x][y]['entry_points'] = entries #зберігаємо точки входу у секторі
                self.grid[x][y]['chests'] = self.place_chests(self.grid[x][y]['tiles']) #розміщуємо сундуки у прохідних тайлах

    def generate_tile_maze(self):
        #генерує локальний лабіринт розміром 9x9 для кожного сектора; повертає двовимірний масив, де 1 — стіна, 0 — прохід
        w, h = 9, 9 #w і h — ширина і висота лабіринту
        maze = [[1]*w for _ in range(h)] #створюємо матрицю, заповнену одиницями (стіни)
        def carve(cx, cy): #рекурсивна функція для створення проходів; cx, cy — поточні координати
            maze[cy][cx] = 0 #позначаємо поточний тайл як прохідний
            dirs = [(1,0),(-1,0),(0,1),(0,-1)] #список напрямків: вправо, вліво, вниз, вгору
            random.shuffle(dirs) #перемішуємо напрямки для випадковості
            for dx, dy in dirs: #перебираємо всі напрямки
                nx, ny = cx + dx*2, cy + dy*2 #обчислюємо координати наступного тайла через одну стіну
                if 0 <= nx < w and 0 <= ny < h and maze[ny][nx] == 1: #перевіряємо, чи новий тайл у межах і ще не відвіданий
                    maze[cy+dy][cx+dx] = 0 #робимо прохід між поточним і наступним тайлом
                    carve(nx, ny) #рекурсивно продовжуємо генерацію з нового тайла
        carve(1,1) #стартуємо генерацію з координат (1,1)
        return maze #повертаємо готовий локальний лабіринт

    def apply_entry_point(self, tiles, direction, off):
        #вирізає отвір у локальному лабіринті tiles на відповідному краю сектора; direction — напрямок, off — зсув
        size = len(tiles) #size — розмір лабіринту (кількість тайлів по одній стороні)
        if direction == 'top': #якщо напрямок "верх", робимо прохід у верхньому рядку
            tiles[0][off] = 0
            tiles[1][off] = 0 #додаємо ще один прохідний тайл під отвором, щоб уникнути застрягання
        elif direction == 'bottom': #якщо напрямок "низ", робимо прохід у нижньому рядку
            tiles[size-1][off] = 0
            tiles[size-2][off] = 0 #додаємо ще один прохідний тайл над отвором, щоб уникнути застрягання
        elif direction == 'left': #якщо напрямок "ліворуч", робимо прохід у першому стовпці
            tiles[off][0] = 0
            tiles[off][1] = 0 #додаємо ще один прохідний тайл праворуч від отвору, щоб уникнути застрягання
        elif direction == 'right': #якщо напрямок "праворуч", робимо прохід у останньому стовпці
            tiles[off][size-1] = 0
            tiles[off][size-2] = 0 #додаємо ще один прохідний тайл ліворуч від отвору, щоб уникнути застрягання

    def place_chests(self, tiles):
        #розміщує до двох сундуків у випадкових прохідних тайлах локального лабіринту tiles
        w = len(tiles[0]) #w — ширина лабіринту
        h = len(tiles) #h — висота лабіринту
        tw = const.sector_size // w #tw — ширина одного тайла у пікселях
        th = const.sector_size // h #th — висота одного тайла у пікселях
        free_tiles = [ #список координат всіх прохідних тайлів (де val == 0)
            (cx, ry)
            for ry, row in enumerate(tiles)
            for cx, val in enumerate(row)
            if val == 0
        ]
        chests = [] #список для сундуків
        for _ in range(const.max_chests_per_sector): #максимум два сундуки
            if not free_tiles: #якщо немає вільних тайлів, завершуємо
                break
            cx, ry = random.choice(free_tiles) #вибираємо випадковий прохідний тайл
            free_tiles.remove((cx, ry)) #видаляємо його зі списку, щоб не повторювати
            px = cx * tw + (tw - 30)//2 #px — координата сундука по x, вирівнюємо по центру тайла
            py = ry * th + (th - 30)//2 #py — координата сундука по y, вирівнюємо по центру тайла
            chests.append(pygame.Rect(px, py, 30, 30)) #створюємо прямокутник-сундук розміром 30x30
        return chests #повертаємо список сундуків

    def generate_full_maze(self):
        #генерує глобальний лабіринт між секторами, видаляючи стіни для створення проходів; використовує алгоритм "відступання назад"
        stack = [] #стек для збереження шляху
        total = const.map_width * const.map_height #total — загальна кількість секторів
        visited = 1 #visited — кількість відвіданих секторів
        cx = random.randrange(const.map_width) #cx — початкова координата x; randrange - вибирає випадкове число від 0 до const.map_width-1
        cy = random.randrange(const.map_height) #cy — початкова координата y
        self.grid[cx][cy]['visited'] = True #позначаємо стартовий сектор як відвіданий
        while visited < total: #поки не відвідані всі сектори
            nbrs = self.get_unvisited_neighbors((cx, cy)) #отримуємо список сусідів, які ще не відвідані
            if nbrs: #якщо є невідвідані сусіди
                nx, ny = random.choice(nbrs) #вибираємо випадкового сусіда
                self.remove_wall((cx, cy), (nx, ny)) #видаляємо стіну між поточним сектором і сусідом
                stack.append((cx, cy)) #додаємо поточний сектор у стек
                cx, cy = nx, ny #переходимо до сусіда
                self.grid[cx][cy]['visited'] = True #позначаємо новий сектор як відвіданий
                visited += 1 #збільшуємо лічильник відвіданих секторів
            else: #якщо немає невідвіданих сусідів
                cx, cy = stack.pop() #повертаємося назад по стеку
        self.add_cycles(const.global_cycle_count) #додаємо додаткові проходи для ускладнення лабіринту

    def get_safe_transition_point(self, sector_pos):
        tiles = self.grid[sector_pos[0]][sector_pos[1]]['tiles'] #отримуємо локальний лабіринт сектора
        tile_w = const.sector_size // const.tile_grid_size #ширина одного тайла у пікселях 
                                               #весь сектор (квадрат) має розмір const.sector_size × const.sector_size пікселів
                                               #він поділений на 9×9 тайлів
                                               #ширина одного тайлу = const.sector_size // 9
                                               #висота одного тайлу = const.sector_size // 9 (оскільки квадрат)
        for y in range(const.tile_grid_size): #перебираємо всі рядки тайлів
            for x in range(const.tile_grid_size): #перебираємо всі стовпці тайлів
                if tiles[y][x] == 0: #якщо тайл прохідний (0)
                    return (x * tile_w + tile_w // 2,  #повертаємо координати центру тайла
                            y * tile_w + tile_w // 2) #плюс половину ширини тайла, щоб отримати центр


    def add_cycles(self, count):
        #додає count додаткових проходів між сусідніми секторами, щоб зробити лабіринт менш лінійним
        attempts = 0 #лічильник спроб
        while attempts < count: #повторюємо, поки не зробимо потрібну кількість проходів
            x = random.randint(0, const.map_width - 2) #x — випадкова координата сектору по x (не останній)
            y = random.randint(0, const.map_height - 2) #y — випадкова координата сектору по y (не останній)
            if random.choice((True, False)): #випадково вибираємо напрямок: вправо або вниз
                nx, ny = x + 1, y #сусідній сектор праворуч
            else:
                nx, ny = x, y + 1 #сусідній сектор знизу
            w1 = self.grid[x][y]['walls'] #w1 — словник стін поточного сектору
            w2 = self.grid[nx][ny]['walls'] #w2 — словник стін сусіднього сектору
            #перевіряємо, чи між секторами є стіни, які можна видалити
            if ((nx==x+1 and w1['right'] and w2['left'])
            or (ny==y+1 and w1['bottom'] and w2['top'])):
                if nx==x+1: #якщо сусід праворуч
                    w1['right']=False; w2['left']=False #видаляємо стіни справа і зліва відповідно
                else: #якщо сусід знизу
                    w1['bottom']=False; w2['top']=False #видаляємо стіни знизу і зверху відповідно
            attempts += 1 #збільшуємо лічильник спроб

    def get_unvisited_neighbors(self, cell):
        #повертає список координат сусідніх секторів, які ще не були відвідані при генерації глобального лабіринту
        x, y = cell #x і y — координати поточного сектору
        nbrs = [] #список невідвіданих сусідів
        if x>0 and not self.grid[x-1][y]['visited']: nbrs.append((x-1,y)) #ліворуч
        if x<const.map_width-1 and not self.grid[x+1][y]['visited']: nbrs.append((x+1,y)) #праворуч
        if y>0 and not self.grid[x][y-1]['visited']: nbrs.append((x,y-1)) #зверху
        if y<const.map_height-1 and not self.grid[x][y+1]['visited']: nbrs.append((x,y+1)) #знизу
        return nbrs #повертаємо список координат

    def remove_wall(self, cur, nxt):
        #видаляє стіну між двома сусідніми секторами cur і nxt; cur і nxt — кортежі координат
        cx, cy = cur #координати поточного сектору
        nx, ny = nxt #координати сусіднього сектору
        wcur = self.grid[cx][cy]['walls'] #словник стін поточного сектору
        wnxt = self.grid[nx][ny]['walls'] #словник стін сусіднього сектору
        if nx == cx+1: #сусід праворуч
            wcur['right'] = False; wnxt['left'] = False #видаляємо стіни справа і зліва
        elif nx == cx-1: #сусід ліворуч
            wcur['left']  = False; wnxt['right']= False #видаляємо стіни зліва і справа
        elif ny == cy+1: #сусід знизу
            wcur['bottom']= False; wnxt['top']  = False #видаляємо стіни знизу і зверху
        else: #сусід зверху
            wcur['top']   = False; wnxt['bottom']= False #видаляємо стіни зверху і знизу

    def get_sector_walls(self, sector_pos):
        #повертає список прямокутників, які представляють глобальні стіни сектора для рендерингу
        x, y = sector_pos #координати сектора
        w = self.grid[x][y]['walls'] #словник стін сектора
        t = 5 #товщина стіни у пікселях
        rects = [] #список прямокутників
        if w['top']:    rects.append(pygame.Rect(0,0,const.sector_size,t)) #стіна зверху
        if w['bottom']: rects.append(pygame.Rect(0,const.sector_size-t,const.sector_size,t)) #стіна знизу
        if w['left']:   rects.append(pygame.Rect(0,0,t,const.sector_size)) #стіна ліворуч
        if w['right']:  rects.append(pygame.Rect(const.sector_size-t,0,t,const.sector_size)) #стіна праворуч
        return rects #повертаємо список прямокутників

    def get_tile_colliders(self, sector_pos):
        #повертає список прямокутників, які представляють непрохідні тайли локального лабіринту для колізій
        x, y = sector_pos #координати сектора
        tiles = self.grid[x][y]['tiles'] #двовимірний масив тайлів сектора
        rects = [] #список прямокутників
        tw = const.sector_size // len(tiles[0]) #ширина одного тайла у пікселях
        th = const.sector_size // len(tiles) #висота одного тайла у пікселях
        for ry, row in enumerate(tiles): #перебираємо всі рядки
            for cx, val in enumerate(row): #перебираємо всі тайли у рядку
                if val == 1: #якщо тайл — стіна
                    rects.append(pygame.Rect(cx*tw, ry*th, tw, th)) #додаємо прямокутник для колізії
        return rects #повертаємо список прямокутників

    def get_chests(self, sector_pos):
        #повертає список сундуків у поточному секторі; sector_pos — координати сектора
        return self.grid[sector_pos[0]][sector_pos[1]]['chests']

    def tre_collect_chest(self, sector_pos, player_rect):
        #перевіряє, чи гравець торкнувся сундука у секторі; якщо так — видаляє цей сундук
        chs = self.grid[sector_pos[0]][sector_pos[1]]['chests'] #список сундуків у секторі
        for c in chs: #перебираємо всі сундуки
            if c.colliderect(player_rect): #перевіряємо зіткнення з гравцем
                chs.remove(c) #видаляємо сундук зі списку
                break #завершуємо цикл після першого знайденого

    def draw_sector(self, screen, sector_pos):
        #відповідає за рендеринг поточного сектора: малює фон, глобальні та локальні стіни, сундуки і фінальний скарб
        x, y = sector_pos #координати сектора
        sector = self.grid[x][y] #дані сектора
        bg = pygame.image.load("pictures/maze_background.png").convert() #завантажуємо зображення фону
        bg = pygame.transform.scale(bg,(const.sector_size,const.sector_size)) #масштабуємо фон до розміру сектора
        screen.blit(bg,(0,0)) #малюємо фон на екрані
        t = 5; cell = const.sector_size//9 #t — товщина стіни, cell — ширина одного тайла
        for direction, off in sector['entry_points']: #перебираємо всі точки входу у сектор
            start = off*cell; end = (off+1)*cell #обчислюємо координати отвору
            if direction == 'top': #якщо отвір зверху
                pygame.draw.rect(screen, colors["ACID_GREEN"], (0,0,start,t)) #малюємо ліву частину стіни
                pygame.draw.rect(screen, colors["ACID_GREEN"], (end,0,const.sector_size-end,t)) #малюємо праву частину стіни
            elif direction == 'bottom': #якщо отвір знизу
                pygame.draw.rect(screen, colors["ACID_GREEN"], (0,const.sector_size-t,start,t))
                pygame.draw.rect(screen, colors["ACID_GREEN"], (end,const.sector_size-t,const.sector_size-end,t))
            elif direction == 'left': #якщо отвір ліворуч
                pygame.draw.rect(screen, colors["ACID_GREEN"], (0,0,t,start))
                pygame.draw.rect(screen, colors["ACID_GREEN"], (0,end,t,const.sector_size-end))
            elif direction == 'right': #якщо отвір праворуч
                pygame.draw.rect(screen, colors["ACID_GREEN"], (const.sector_size-t,0,t,start))
                pygame.draw.rect(screen, colors["ACID_GREEN"], (const.sector_size-t,end,t,const.sector_size-end))
        tw = const.sector_size//9; th = const.sector_size//9 #tw і th — розміри тайла у пікселях
        for ry, row in enumerate(sector['tiles']): #перебираємо всі рядки локального лабіринту
            for cx, val in enumerate(row): #перебираємо всі тайли у рядку
                if val == 1: #якщо тайл — стіна
                    pygame.draw.rect(screen, colors["DEEP_PINK"], (cx*tw, ry*th, tw, th)) #малюємо стіну
        for chest in sector['chests']: #перебираємо всі сундуки у секторі
            pygame.draw.rect(screen, colors["YELLOW"], chest) #малюємо сундук
        if (x,y) == self.treasure_pos: #якщо сектор містить фінальний скарб
            pygame.draw.circle(screen, colors["GREEN"], (const.sector_size//2,const.sector_size//2),20) #малюємо скарб у центрі сектора
