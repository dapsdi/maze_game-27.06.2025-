#settings/constants.py#
#основні налаштування

#назва вікна
title = "Гра-лабіринт"

#розміри вікна
window_width = 900
window_height = 900

#розміри мапи в секторах
map_width = 10
map_height = 10
tile_grid_size = 9  #розмір сітки тайлів у секторі
#чому 9: у методі generate_tile_maze створюється локальний лабіринт розміром 9х9
#кожен сектор на карті(в глобальній сітці екторів) має власний розмір(міні карту) із 9 тайлів

#перелік доступних біомів
BIOMES = {
    "jungle": {
        "background": "pictures/jungle_background.png",
        "wall_color":  (66, 32, 128),
    },

    "swamp": {
        "background": "pictures/swamp_background.png",
        "wall_color":  (72, 66, 98),
    },

    "desert": {
        "background": "pictures/desert_background.png",
        "wall_color":  (69, 124, 168),
    },

    "mountain": {
        "background": "pictures/mountain_background.png",
        "wall_color":  (80, 0, 0),
    },

    "cave": {
        "background": "pictures/cave_background.png",
        "wall_color":  (59, 73, 89),
    },
}

#мінімальний/максимальний зсув входу від краю сектора
entry_offset_min = 2  
entry_offset_max = 6 

#максимальна кількість скринь у секторі
max_chests_per_sector = 3  

#кількість додаткових циклів для ускладнення глобального лабіринту
global_cycle_count = 40

#кількість кадрів за секунду
fps = 60

#розміри тайлу та сектору встановлюються динамічно у core/game.py
tile_px = None
sector_size = None  