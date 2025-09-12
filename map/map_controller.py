import os
import glob
import pygame
import random
import settings.constants as const  #імпортуємо глобальні константи з settings
from ui.colors import colors        #кольори для малювання
from settings.constants import BIOMES  #словар з даними про біоми

class MapController:
    def __init__(self):
        #створюємо двовимірний масив grid який містить дані про кожен сектор карти
        self.grid = [
            [
                {
                    'visited': False,  #чи вже відвідано цей сектор при генерації лабіринту
                    'walls': {'top': True, 'bottom': True, 'left': True, 'right': True}, #зовнішні стіни сектора
                    'tiles': self.generate_tile_maze(),  #локальний лабіринт усередині сектора
                    'chests': [],  #квіти або сундуки у секторі
                    'entry_points': []  #точки входів/виходів у сектор
                }
                for _ in range(const.map_height)
            ]
            for _ in range(const.map_width)
        ]

        #позиція головного скарбу на карті
        self.treasure_pos = (
            random.randrange(const.map_width),
            random.randrange(const.map_height)
        )

        #створюємо карту біомів (спочатку пуста)
        self.biome_map = [[None]*const.map_height for _ in range(const.map_width)]
        self.assign_biomes()  #призначаємо біоми

        #завантажуємо картинки квітів
        self.flower_images = []
        self.ui_flower_frames = []
        self.load_flower_images()

        #копіюємо інформацію про біом у кожен сектор
        for x in range(const.map_width):
            for y in range(const.map_height):
                self.grid[x][y]['biome'] = self.biome_map[x][y]

        #створюємо глобальний лабіринт між секторами
        self.generate_full_maze()

        #створюємо входи і розміщуємо квіти у кожному секторі
        for x in range(const.map_width):
            for y in range(const.map_height):
                entries = []
                for direction, is_wall in self.grid[x][y]['walls'].items():
                    if not is_wall:
                        offset = random.randint(const.entry_offset_min, const.entry_offset_max)
                        entries.append((direction, offset))
                        self.apply_entry_point(self.grid[x][y]['tiles'], direction, offset)
                self.grid[x][y]['entry_points'] = entries
                self.grid[x][y]['chests'] = self.place_chests(self.grid[x][y]['tiles'])

    def load_flower_images(self):
        #шукаємо картинки квітів, пріоритет у assets/flowers/realistic_flowers
        specific_dir = os.path.join("assets", "flowers", "realistic_flowers")
        paths = []
        if os.path.isdir(specific_dir):
            paths = sorted(glob.glob(os.path.join(specific_dir, "flower_*.png")))
        #якщо нема у realistic_flowers, шукаємо будь-де у assets/flowers
        if not paths:
            base = "assets/flowers"
            exts = ("*.png", "*.jpg", "*.jpeg", "*.gif")
            if os.path.isdir(base):
                for root, dirs, files in os.walk(base):
                    for ext in exts:
                        paths.extend(glob.glob(os.path.join(root, ext)))
            paths = sorted(set(paths))
        if not paths:
            self.flower_images = []
            self.ui_flower_frames = []
            return
        #визначаємо розміри для секторів та для ui
        tile_px = const.tile_px if const.tile_px else (const.sector_size // const.tile_grid_size if const.sector_size else 32)
        flower_display_size = max(12, int(tile_px * 0.6))
        ui_size = max(12, int(tile_px * 0.35))
        loaded = []
        for p in paths:
            try:
                img = pygame.image.load(p).convert_alpha()
            except Exception:
                continue
            img_tile = pygame.transform.smoothscale(img, (flower_display_size, flower_display_size))
            loaded.append(img_tile)
        self.flower_images = loaded
        #створюємо ui-фрейми (до 5 картинок)
        ui_frames = []
        if loaded:
            for i in range(5):
                src = loaded[i % len(loaded)]
                ui_frames.append(pygame.transform.smoothscale(src, (ui_size, ui_size)))
        self.ui_flower_frames = ui_frames

    def generate_tile_maze(self):
        #створює локальний лабіринт у секторі методом рекурсивного проходу
        w, h = 9, 9
        maze = [[1]*w for _ in range(h)]
        def carve(cx, cy):
            maze[cy][cx] = 0
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = cx + dx*2, cy + dy*2
                if 0 <= nx < w and 0 <= ny < h and maze[ny][nx] == 1:
                    maze[cy+dy][cx+dx] = 0
                    carve(nx, ny)
        carve(1,1)
        return maze

    def apply_entry_point(self, tiles, direction, off):
        #створює прохід у локальному лабіринті
        size = len(tiles)
        if direction == 'top':
            tiles[0][off] = 0
            tiles[1][off] = 0
        elif direction == 'bottom':
            tiles[size-1][off] = 0
            tiles[size-2][off] = 0
        elif direction == 'left':
            tiles[off][0] = 0
            tiles[off][1] = 0
        elif direction == 'right':
            tiles[off][size-1] = 0
            tiles[off][size-2] = 0

    def assign_biomes(self):
        #призначає випадкові біоми кожному сектору
        names = list(BIOMES.keys())
        coordinates = [(x, y) for x in range(const.map_width) for y in range(const.map_height)]
        random.shuffle(coordinates)
        for name, coord in zip(names, coordinates):
            x, y = coord
            self.biome_map[x][y] = name
        for x in range(const.map_width):
            for y in range(const.map_height):
                if self.biome_map[x][y] is None:
                    self.biome_map[x][y] = random.choice(names)

    def get_biome(self, sector_pos):
        #повертає назву біома за координатою сектора
        x, y = sector_pos
        return self.biome_map[x][y]

    def place_chests(self, tiles):
        #розміщує квіти у секторі на випадкових вільних клітинках
        w = len(tiles[0])
        h = len(tiles)
        tw = const.sector_size // w
        th = const.sector_size // h
        free_tiles = [
            (cx, ry)
            for ry, row in enumerate(tiles)
            for cx, val in enumerate(row)
            if val == 0
        ]
        chests = []
        if not free_tiles or not self.flower_images:
            return []
        for _ in range(const.max_chests_per_sector):
            if not free_tiles:
                break
            cx, ry = random.choice(free_tiles)
            free_tiles.remove((cx, ry))
            flower_img = random.choice(self.flower_images)
            fw, fh = flower_img.get_size()
            px = cx * tw + (tw - fw)//2
            py = ry * th + (th - fh)//2
            rect = pygame.Rect(px, py, fw, fh)
            chests.append({'rect': rect, 'image': flower_img})
        return chests

    def generate_full_maze(self):
        #створює глобальний лабіринт між секторами за алгоритмом dfs
        stack = []
        total = const.map_width * const.map_height
        visited = 1
        cx = random.randrange(const.map_width)
        cy = random.randrange(const.map_height)
        self.grid[cx][cy]['visited'] = True
        while visited < total:
            nbrs = self.get_unvisited_neighbors((cx, cy))
            if nbrs:
                nx, ny = random.choice(nbrs)
                self.remove_wall((cx, cy), (nx, ny))
                stack.append((cx, cy))
                cx, cy = nx, ny
                self.grid[cx][cy]['visited'] = True
                visited += 1
            else:
                cx, cy = stack.pop()
        self.add_cycles(const.global_cycle_count)

    def get_safe_transition_point(self, sector_pos):
        #повертає координати безпечної точки усередині сектора
        tiles = self.grid[sector_pos[0]][sector_pos[1]]['tiles']
        tile_w = const.sector_size // const.tile_grid_size
        for y in range(const.tile_grid_size):
            for x in range(const.tile_grid_size):
                if tiles[y][x] == 0:
                    return (x * tile_w + tile_w // 2,
                            y * tile_w + tile_w // 2)

    def add_cycles(self, count):
        #додає додаткові проходи у глобальний лабіринт для різноманітності
        attempts = 0
        while attempts < count:
            x = random.randint(0, const.map_width - 2)
            y = random.randint(0, const.map_height - 2)
            if random.choice((True, False)):
                nx, ny = x + 1, y
            else:
                nx, ny = x, y + 1
            w1 = self.grid[x][y]['walls']
            w2 = self.grid[nx][ny]['walls']
            if ((nx==x+1 and w1['right'] and w2['left'])
            or (ny==y+1 and w1['bottom'] and w2['top'])):
                if nx==x+1:
                    w1['right']=False; w2['left']=False
                else:
                    w1['bottom']=False; w2['top']=False
            attempts += 1

    def get_unvisited_neighbors(self, cell):
        #повертає список сусідніх секторів які ще не були відвідані
        x, y = cell
        nbrs = []
        if x>0 and not self.grid[x-1][y]['visited']: nbrs.append((x-1,y))
        if x<const.map_width-1 and not self.grid[x+1][y]['visited']: nbrs.append((x+1,y))
        if y>0 and not self.grid[x][y-1]['visited']: nbrs.append((x,y-1))
        if y<const.map_height-1 and not self.grid[x][y+1]['visited']: nbrs.append((x,y+1))
        return nbrs

    def remove_wall(self, cur, nxt):
        #знімає стіну між двома сусідніми секторами
        cx, cy = cur
        nx, ny = nxt
        wcur = self.grid[cx][cy]['walls']
        wnxt = self.grid[nx][ny]['walls']
        if nx == cx+1:
            wcur['right'] = False; wnxt['left'] = False
        elif nx == cx-1:
            wcur['left']  = False; wnxt['right']= False
        elif ny == cy+1:
            wcur['bottom']= False; wnxt['top']  = False
        else:
            wcur['top']   = False; wnxt['bottom']= False

    def get_sector_walls(self, sector_pos):
        #повертає список прямокутників стін сектора
        x, y = sector_pos
        w = self.grid[x][y]['walls']
        t = 5
        rects = []
        if w['top']:    rects.append(pygame.Rect(0,0,const.sector_size,t))
        if w['bottom']: rects.append(pygame.Rect(0,const.sector_size-t,const.sector_size,t))
        if w['left']:   rects.append(pygame.Rect(0,0,t,const.sector_size))
        if w['right']:  rects.append(pygame.Rect(const.sector_size-t,0,t,const.sector_size))
        return rects

    def get_tile_colliders(self, sector_pos):
        #повертає список прямокутників стін у локальному лабіринті
        x, y = sector_pos
        tiles = self.grid[x][y]['tiles']
        rects = []
        tw = const.sector_size // len(tiles[0])
        th = const.sector_size // len(tiles)
        for ry, row in enumerate(tiles):
            for cx, val in enumerate(row):
                if val == 1:
                    rects.append(pygame.Rect(cx*tw, ry*th, tw, th))
        return rects

    def get_chests(self, sector_pos):
        #повертає список квітів у секторі
        return self.grid[sector_pos[0]][sector_pos[1]]['chests']

    def tre_collect_chest(self, sector_pos, player_rect):
        #перевіряє чи гравець зібрав квіти, повертає кількість зібраних
        x, y = sector_pos
        chs = self.grid[x][y]['chests']
        removed = 0
        remaining = []
        for c in chs:
            rect = c['rect'] if isinstance(c, dict) and 'rect' in c else c
            if player_rect.colliderect(rect):
                removed += 1
            else:
                remaining.append(c)
        if removed:
            self.grid[x][y]['chests'] = remaining
        return removed

    def draw_sector(self, screen, sector_pos):
        #малює сектор на екрані
        x, y = sector_pos
        sector = self.grid[x][y]
        biome_name = sector["biome"]
        parameters = BIOMES[biome_name]
        background_path = parameters["background"]
        wall_color = parameters["wall_color"]
        #фон
        bg = pygame.image.load(background_path).convert()
        bg = pygame.transform.scale(bg, (const.sector_size, const.sector_size))
        screen.blit(bg, (0,0))
        #стіни входів
        t = 5; cell = const.sector_size // const.tile_grid_size
        for direction, off in sector['entry_points']:
            start = off*cell; end = (off+1)*cell
            if direction == 'top':
                pygame.draw.rect(screen, wall_color, (0,0,start,t))
                pygame.draw.rect(screen, wall_color, (end,0,const.sector_size-end,t))
            elif direction == 'bottom':
                pygame.draw.rect(screen, wall_color, (0,const.sector_size-t,start,t))
                pygame.draw.rect(screen, wall_color, (end,const.sector_size-t,const.sector_size-end,t))
            elif direction == 'left':
                pygame.draw.rect(screen, wall_color, (0,0,t,start))
                pygame.draw.rect(screen, wall_color, (0,end,t,const.sector_size-end))
            elif direction == 'right':
                pygame.draw.rect(screen, wall_color, (const.sector_size-t,0,t,start))
                pygame.draw.rect(screen, wall_color, (const.sector_size-t,end,t,const.sector_size-end))
        #локальні стіни тайлів
        tw = const.sector_size // const.tile_grid_size
        th = tw
        for ry, row in enumerate(sector['tiles']):
            for cx, val in enumerate(row):
                if val == 1:
                    pygame.draw.rect(screen, wall_color, (cx*tw, ry*th, tw, th))
        #малюємо квіти
        for chest in sector['chests']:
            if isinstance(chest, dict) and 'image' in chest and 'rect' in chest:
                screen.blit(chest['image'], chest['rect'])
            else:
                rect = chest['rect'] if isinstance(chest, dict) and 'rect' in chest else chest
                if isinstance(rect, pygame.Rect):
                    pygame.draw.rect(screen, colors["YELLOW"], rect)
        #малюємо головний скарб
        if (x,y) == self.treasure_pos:
            pygame.draw.circle(screen, colors["GREEN"], (const.sector_size//2,const.sector_size//2), 20)
