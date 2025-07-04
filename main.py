#main.py#
import pygame
from settings import *
from player import Player
from map import Map
from ui import draw_button

pygame.init()

#ми починаємо в режимі показу всієї карти, тому full_screen = True
full_screen = True
#спочатку відкриваємо вікно розміром усієї карти
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(title)
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)
button_font = pygame.font.SysFont(None, 28)

#кнопка «почати гру» розташована по центру внизу екрану
start_button = pygame.Rect(
    screen_width // 2 - 100,   #зрушення вліво на половину ширини кнопки
    screen_height - 70,        #70 пікселів від низу
    200, 50                    #розміри кнопки (ширина, висота)
)

#створюємо об’єкти гравця та карти
player = Player(sector_size // 2, sector_size // 2)
game_map = Map()

in_game = False   #поки що ми не в ігровому режимі
running = True    #флаг основного циклу

while running:
    clock.tick(fps)  #обмежуємо швидкість циклу до fps кадрів на секунду

    #обробляємо всі події, які відбулися з моменту останньої ітерації
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   #якщо натиснули на хрестик, завершуємо програму

        elif event.type == pygame.MOUSEBUTTONDOWN and not in_game:
            #якщо ми в стартовому режимі і клікнули по кнопці, починаємо гру
            if start_button.collidepoint(event.pos):
                in_game = True
                full_screen = False
                #міняємо розмір вікна на один сектор, щоб реалізувати камеру
                screen = pygame.display.set_mode((sector_size, sector_size))
                pygame.display.set_caption(title)

    #якщо досі в стартовому режимі (не почали гру), малюємо всю карту
    if not in_game:
        screen.fill(colors["BLACK"])  #фон чорний, щоб сектори краще виділялися

        #проходимо по всіх секторах карти в двох циклах
        for x in range(map_width):
            for y in range(map_height):
                px, py = x * sector_size, y * sector_size
                #малюємо фон сектора жовтим
                pygame.draw.rect(screen, colors["YELLOW"], (px, py, sector_size, sector_size))

                #перевіряємо, які стіни залишилися в цьому секторі
                w = game_map.sectors[x][y]['walls']
                t = 5  #товщина стіни в пікселях

                #малюємо верхню стіну, якщо вона True
                if w['top']:
                    pygame.draw.rect(screen, colors["GRAY"], (px, py, sector_size, t))
                #малюємо нижню стіну
                if w['bottom']:
                    pygame.draw.rect(screen, colors["GRAY"], (px, py + sector_size - t, sector_size, t))
                #малюємо ліву стіну
                if w['left']:
                    pygame.draw.rect(screen, colors["GRAY"], (px, py, t, sector_size))
                #малюємо праву стіну
                if w['right']:
                    pygame.draw.rect(screen, colors["GRAY"], (px + sector_size - t, py, t, sector_size))

                #якщо тут скарб, малюємо його зеленим колом в центрі сектора
                if (x, y) == game_map.treasure_position:
                    pygame.draw.circle(
                        screen, colors["GREEN"],
                        (px + sector_size // 2, py + sector_size // 2),
                        20
                    )

        #після того як відмалювали всі сектори, малюємо кнопку
        draw_button(screen, start_button, "Почати гру", button_font)
        pygame.display.flip()  #показуємо результат
        continue  #переходимо до наступної ітерації без решти малювання

    #якщо ми вже в ігровому режимі, починаємо звичний цикл руху й камери

    keys = pygame.key.get_pressed()  #отримуємо стан всіх клавіш

    #дізнаємося, в якому секторі зараз гравець (x//sector_size, y//sector_size)
    current_sector = player.get_sector_position()

    #будуємо прямокутник, що описує межі поточного сектора в глобальних координатах
    sector_rect = pygame.Rect(
        current_sector[0] * sector_size,
        current_sector[1] * sector_size,
        sector_size,
        sector_size
    )

    #отримуємо список стін поточного сектора (pygame.Rect для зіткнень)
    walls = game_map.get_walls(current_sector)

    #рухаємо гравця тільки перевіряючи стіни, без обмеження по межах
    player.move(keys, walls)

    #тепер перевіряємо, чи вийшов гравець за межі поточного сектора
    px, py = current_sector
    transitioned = False  #флаг переходу в новий сектор

    #якщо x гравця менше лівої межі сектора (px*sector_size)
    if player.x < px * sector_size:
        if px > 0:
            px -= 1
            #телепортуємо гравця праворуч в новому секторі
            player.x = px * sector_size + sector_size - player.size
            transitioned = True

    #якщо правий край гравця за межами правої рамки сектора
    elif player.x + player.size > (px + 1) * sector_size:
        if px < map_width - 1:
            px += 1
            #ставимо гравця зліва
            player.x = px * sector_size
            transitioned = True

    #перевіряємо вихід угору
    if player.y < py * sector_size:
        if py > 0:
            py -= 1
            #ставимо гравця знизу
            player.y = py * sector_size + sector_size - player.size
            transitioned = True

    #перевіряємо вихід вниз
    elif player.y + player.size > (py + 1) * sector_size:
        if py < map_height - 1:
            py += 1
            #ставимо гравця зверху
            player.y = py * sector_size
            transitioned = True

    #якщо був перехід, оновлюємо номер сектору
    if transitioned:
        current_sector = (px, py)

    #камера зміщується, щоб сектор гравця опинився в області 0,0—sector_size
    camera_offset = (current_sector[0] * sector_size, current_sector[1] * sector_size)

    #малюємо чорний фон для нового кадру
    screen.fill(colors["BLACK"])
    #малюємо поточний сектор із його стінами та скарбом
    game_map.draw_current_sector(screen, current_sector)
    #малюємо гравця з урахуванням зсуву камери
    player.draw(screen, camera_offset)

    pygame.display.flip()  #оновлюємо вікно

pygame.quit()  #виходимо з pygame
