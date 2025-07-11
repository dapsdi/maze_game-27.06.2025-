from settings.constants import sector_size

class Camera:
    def __init__(self, player):
        #зберігаємо гравця, щоб знати його сектор
        self.player = player
        self.offset = (0, 0)  #зсув відносно глобальної карти

    def update(self):
        #розраховуємо зсув так, щоб сектор гравця опинявся в (0,0) на екрані
        sector_pos = self.player.get_sector()
        self.offset = (sector_pos[0] * sector_size, sector_pos[1] * sector_size)
