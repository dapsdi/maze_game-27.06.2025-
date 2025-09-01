import pygame
from settings.constants import *
from core.game import Game

#ініціалізуємо pygame
pygame.init()

#створюємо екземпляр гри
game = Game()
#запускаємо головний цикл гри
game.run()

#після завершення циклу — вихід з pygame
pygame.quit()

        