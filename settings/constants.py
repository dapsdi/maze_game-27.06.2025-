import pygame

# основні налаштування
# назва вікна
title = "Гра-лабіринт"

# розміри вікна
window_width = 900
window_height = 900

# розміри мапи в секторах
map_width = 10
map_height = 10
tile_grid_size = 9  # розмір сітки тайлів у секторі
# чому 9: у методі generate_tile_maze створюється локальний лабіринт розміром 9х9
# кожен сектор на карті(в глобальній сітці екторів) має власний розмір(міні карту) із 9 тайлів

# перелік доступних біомів
BIOMES = {
    "plains": {
        "background": "pictures/biomes/plains_background.png",
        "wall_color":  (141, 25, 83),
    },
    "jungle": {
        "background": "pictures/biomes/jungle_background.png",
        "wall_color":  (66, 32, 128),
    },

    "swamp": {
        "background": "pictures/biomes/swamp_background.png",
        "wall_color":  (72, 66, 98),
    },

    "desert": {
        "background": "pictures/biomes/desert_background.png",
        "wall_color":  (69, 124, 168),
    },

    "mountain": {
        "background": "pictures/biomes/mountain_background.png",
        "wall_color":  (80, 0, 0),
    },

    "cave": {
        "background": "pictures/biomes/cave_background.png",
        "wall_color":  (59, 73, 89),
    },
}

# константи для розмірів та відступів
MENU_WIDTH = 600
MENU_HEIGHT = 600
MENU_BORDER_WIDTH = 4

TITLE_FONT_SIZE = 48
FONT_SIZE = 32
SMALL_FONT_SIZE = 24

MENU_PADDING = 50
TITLE_TOP_MARGIN = 20
FLOWERS_TOP_MARGIN = 70
RECIPES_TOP_MARGIN = 120
RECIPE_HEIGHT = 60
RECIPE_WIDTH = 500
RECIPE_SPACING = 80
RECIPE_PADDING = 10
RECIPE_BORDER_WIDTH = 2

DESCRIPTION_HEIGHT = 40
DESCRIPTION_TOP_MARGIN = 20

INSTRUCTION_BOTTOM_MARGIN = 40

# Кольори
MENU_BG_COLOR = "#202040"
MENU_BORDER_COLOR = "#505080"
RECIPE_BG_COLOR = "#464664"
RECIPE_HOVER_COLOR = "#606080"
RECIPE_CANT_AFFORD_COLOR = "#833939"
RECIPE_CANT_AFFORD_HOVER_COLOR = "#9C4545"
RECIPE_BORDER_COLOR = "#64648c"
DESCRIPTION_BG_COLOR = "#323250"
DESCRIPTION_BORDER_COLOR = "#505078"
TEXT_COLOR_CANT_AFFORD = "#A73A3A"
KEY_HINT_COLOR = "#b4b4b4"
INSTRUCTION_COLOR = "#c8c8c8"

# кольори
colors = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 120, 255),
    "YELLOW": (255, 255, 0),
    "GRAY": (150, 150, 150),
    "PURPLE": (150, 50, 200),
    "ORANGE": (255, 165, 0),
    "BROWN": (165, 42, 42),
    "PINK": (255, 192, 203)
}

# типи зіллів
POTION_TYPES = {
    "SPEED": 0,
    "INVISIBILITY": 1, 
    "TELEPORT": 2,
    "INVULNERABILITY": 3,  # замість FIRE_RESISTANCE
    "FLOWER_DETECTOR": 4
}

# кольори зіллів
POTION_COLORS = {
    "SPEED": "#688EF0",        
    "INVISIBILITY": "#DDD0FD", 
    "TELEPORT": "#E96DBA",   
    "INVULNERABILITY": "#DD6F3F",  # новий колір
    "FLOWER_DETECTOR": "#3DCC16"  
}

# тривалість ефектів зіллів (в мілісекундах)
POTION_DURATIONS = {
    "SPEED": 5000,           # 5 секунд
    "INVISIBILITY": 7000,    # 7 секунд
    "INVULNERABILITY": 10000,# 10 секунд
    "FLOWER_DETECTOR": 120000 # 120 секунд (2 хвилини)
}

# вартість крафтингу зіллів (в квітках)
POTION_COSTS = {
    "SPEED": 3,
    "INVISIBILITY": 5,
    "TELEPORT": 7,
    "INVULNERABILITY": 4,
    "FLOWER_DETECTOR": 20  # змінили вартість
}

# клавіші для використання зіллів
POTION_KEYS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]

# шанс появи квітки в кімнаті
FLOWER_SPAWN_CHANCE = 0.7
# максимальна кількість квіток в кімнаті
MAX_FLOWERS_PER_ROOM = 3
# початкова кількість здоров'я гравця
PLAYER_MAX_HEALTH = 3
# швидкість гравця
PLAYER_SPEED = 200
# швидкість ворога
ENEMY_SPEED = 200
# шанс появи ворога
ENEMY_SPAWN_CHANCE = 0.3
# урон ворога
ENEMY_DAMAGE = 1
# час невразливості після отримання урону (в секундах)
INVINCIBILITY_DURATION = 1.0

# константи для екрану налаштувань
SETTINGS_MENU_WIDTH = 600
SETTINGS_MENU_HEIGHT = 500
SETTINGS_MENU_BORDER_WIDTH = 4
SETTINGS_TITLE_FONT_SIZE = 48
SETTINGS_FONT_SIZE = 32
SETTINGS_SMALL_FONT_SIZE = 24
SETTINGS_MENU_PADDING = 50
SETTINGS_TITLE_TOP_MARGIN = 20
SETTINGS_SLIDER_HEIGHT = 10
SETTINGS_SLIDER_WIDTH = 400
SETTINGS_SLIDER_TOP_MARGIN = 40
SETTINGS_SLIDER_SPACING = 80
SETTINGS_BUTTON_WIDTH = 150
SETTINGS_BUTTON_HEIGHT = 50
SETTINGS_BUTTON_SPACING = 50
SETTINGS_BUTTON_BOTTOM_MARGIN = 40

# кольори для налаштувань
SETTINGS_MENU_BG_COLOR = "#202040"
SETTINGS_MENU_BORDER_COLOR = "#505080"
SETTINGS_SLIDER_BG_COLOR = "#464664"
SETTINGS_SLIDER_BORDER_COLOR = "#64648c"
SETTINGS_SLIDER_KNOB_COLOR = "#688EF0"
SETTINGS_BUTTON_COLOR = "#464664"
SETTINGS_BUTTON_APPLY_COLOR = "#3DCC16"
SETTINGS_BUTTON_CLOSE_COLOR = "#DD6F3F"
SETTINGS_BUTTON_ADMIN_COLOR = "#E96DBA"
SETTINGS_BUTTON_HOVER_COLOR = "#8080A0"
SETTINGS_BUTTON_BORDER_COLOR = "#64648c"

# мінімальний/максимальний зсув входу від краю сектора
entry_offset_min = 2  
entry_offset_max = 6 

# максимальна кількість скринь у секторі
max_chests_per_sector = 3  

# кількість додаткових циклів для ускладнення глобального лабіринту
global_cycle_count = 40

# кількість кадрів за секунду
fps = 60

# розміри тайлу та сектору встановлюються динамічно у core/game.py
tile_px = None
sector_size = None