#settings.py#
#всі розміри,кольори та назви -- 

#розміри одного сектора (клітинки лабіринту)
sector_size = 200

#розміри всієї карти (кідькість секторів по горизонталі та вертикалі)
map_width = 9   
map_height = 5

#розміри вікна гри
screen_width = sector_size * map_width
screen_height = sector_size * map_height

fps = 60

#кольори
colors = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "DARK_GREEN": (0, 180, 0),
    "DARK_RED": (180, 0, 0),
    "GRAY": (100, 100, 100),
}

#назва гри
title = "Гра Лабіринт"