#core/game.py#

import pygame
import settings.constants as const
from map.map_controller import MapController
from entities.player import Player
from core.camera import Camera
from ui.start_screen import show_start_screen
from ui.settings_screen import show_settings_screen
from ui.craft_screen import show_craft_menu
from entities.fairy import Fairy
from entities.workbench import Workbench
from core.save_load import SaveLoadSystem
from entities.npc import NPC
from ui.dialogue import DialogueSystem
from quests.quest import Quest, QuestManager
from events.event_manager import EventManager
from entities.potion_inventory import PotionInventory
import random

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(const.title)

        self.screen = pygame.display.set_mode((const.window_width, const.window_height))

        #розрахунок розмірів тайла і сектора
        const.tile_px = min(const.window_width, const.window_height) // const.tile_grid_size
        const.sector_size = const.tile_px * const.tile_grid_size

        self.map_controller = MapController()

        #шукаємо стартовий сектор у біомі plains
        start_sector = None
        for x in range(const.map_width):
            for y in range(const.map_height):
                if self.map_controller.get_biome((x, y)) == "plains":
                    start_sector = (x, y)
                    break
            if start_sector:
                break
        if start_sector is None:
            start_sector = (0, 0)

        #створюємо гравця у стартовому секторі
        safe_pos = self.find_safe_position(start_sector)
        self.player = Player(start_sector=start_sector, game=self, pos = safe_pos)
        #створюємо фею, яка прив'язана до гравця
        self.fairy = Fairy("assets/entities/green blob fairy", self.player)
        self.camera = Camera()
        self.clock = pygame.time.Clock()

        #створюємо один верстак на карті
        self.workbench = Workbench((300, 300))

        self.save_system = SaveLoadSystem()
        self.quest_manager = QuestManager()
        self.dialogue_system = DialogueSystem()
        self.event_manager = EventManager()
        
        #створюємо групи NPC
        self.npcs = pygame.sprite.Group()
        self.spawn_npcs()

        #прямокутник для кнопки налаштувань
        self.setting_button = pygame.Rect(const.window_width - 60, 20, 40, 40)

        #кадри квітки для UI
        self.ui_frames = self.map_controller.ui_flower_frames or []
        self.ui_frame_index = 0
        self.ui_timer = 0.0
        self.ui_frame_speed = 0.18

        #показуємо стартовий екран
        show_start_screen(self.screen)
        
        #завантажуємо тестові квести
        self.setup_test_quests()

    def find_safe_position(self, sector):
        walls = self.map_controller.get_sector_walls(sector) + \
                self.map_controller.get_tile_colliders(sector)
        
        # Використовуємо розміри хітбоксу гравця
        player_width = 30
        player_height = 30
        
        for _ in range(100):
            x = random.randint(50, const.sector_size - 50)
            y = random.randint(50, const.sector_size - 50)
            test_rect = pygame.Rect(x - player_width//2, y - player_height//2, 
                                  player_width, player_height)
            
            collision = False
            for wall in walls:
                if test_rect.colliderect(wall):
                    collision = True
                    break
                    
            if not collision:
                return (x, y)
        
        return (const.sector_size // 2, const.sector_size // 2)


    def spawn_npcs(self):
        #спавнимо NPC у випадкових місцях
        dialogues = [
            ("Villager", "Hello traveler! Welcome to our village."),
            ("Villager", "The maze can be dangerous, be careful!"),
            ("Villager", "Good luck on your journey!")
        ]
        
        for _ in range(3):  #3 NPC для початку
            x = random.randint(50, const.sector_size - 50)
            y = random.randint(50, const.sector_size - 50)
            self.npcs.add(NPC(x, y, "villager", dialogues))

    def setup_test_quests(self):
        #створюємо тестові квести
        flower_quest = Quest(
            "collect_flowers",
            "Collect Flowers",
            "Gather 10 flowers from the maze",
            [{
                "type": "collect",
                "target": "flower",
                "description": "Collect 10 flowers",
                "progress": 0,
                "required": 10,
                "completed": False
            }]
        )
        flower_quest.rewards = {"flowers": 20}
        self.quest_manager.add_quest(flower_quest)
        self.quest_manager.start_quest("collect_flowers")

    def find_safe_position(self, sector):
        """знаходить безпечну позицію у секторі без колізій зі стінами"""
        walls = self.map_controller.get_sector_walls(sector) + \
                self.map_controller.get_tile_colliders(sector)
        
        #спробуємо кілька випадкових позицій
        for _ in range(100):
            x = random.randint(50, const.sector_size - 50)
            y = random.randint(50, const.sector_size - 50)
            test_rect = pygame.Rect(x - 25, y - 25, 50, 50)
            
            #перевіряємо колізії зі всіма стінами
            collision = False
            for wall in walls:
                if test_rect.colliderect(wall):
                    collision = True
                    break
                    
            if not collision:
                return (x, y)
        
        #якщо не знайшли безпечну позицію, повертаємо центр
        return (const.sector_size // 2, const.sector_size // 2)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(const.fps) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    #натиснута e
                    elif event.key == pygame.K_e:
                        #якщо гравець біля верстака
                        if self.player.rect.colliderect(self.workbench.rect):
                            show_craft_menu(self)  #виправлено: передаємо тільки self
                    #обробка використання зілль за допомогою клавіш 1-5
                    elif event.key in const.POTION_KEYS:
                        index = const.POTION_KEYS.index(event.key)
                        potion_types = list(self.player.potion_inventory.inventory.keys())
                        if index < len(potion_types):
                            potion_type = potion_types[index]
                            if self.player.potion_inventory.use_potion(potion_type):
                                #якщо використали зілля швидкості, активуємо фею
                                if potion_type == "SPEED":
                                    self.fairy.activate(7.0)
                    #збереження/завантаження
                    elif event.key == pygame.K_F5:
                        self.save_system.save_game(self.player, self.map_controller)
                    elif event.key == pygame.K_F9:
                        self.save_system.load_game(self.player, self.map_controller)
                    #діалоги
                    elif event.key == pygame.K_SPACE and self.dialogue_system.active:
                        self.dialogue_system.next_line()
                    #взаємодія з NPC
                    elif event.key == pygame.K_f and not self.dialogue_system.active:
                        for npc in self.npcs:
                            if npc.can_interact(self.player):
                                self.dialogue_system.start_dialogue(npc.get_dialogues())
                                break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #перевірка кліку на кнопку налаштувань
                    if self.setting_button.collidepoint(event.pos):
                        show_settings_screen(self.screen, self.player)

            #оновлюємо гру тільки якщо діалог не активний
            if not self.dialogue_system.active:
                sx, sy = self.player.get_sector()
                global_walls = self.map_controller.get_sector_walls((sx, sy))
                tile_walls = self.map_controller.get_tile_colliders((sx, sy))
                walls = global_walls + tile_walls

                # Оновлення гравця і феї
                self.player.update(dt, walls)
                self.fairy.update(dt)

                # Перевірка переходів між секторами
                new_sector = None
                sx, sy = self.player.get_sector()
                # Використовуємо hitbox замість rect для перевірки переходів
                if self.player.hitbox.right < 0 and sx > 0:
                    new_sector = (sx - 1, sy)
                elif self.player.hitbox.left > const.sector_size and sx < const.map_width - 1:
                    new_sector = (sx + 1, sy)
                elif self.player.hitbox.bottom < 0 and sy > 0:
                    new_sector = (sx, sy - 1)
                elif self.player.hitbox.top > const.sector_size and sy < const.map_height - 1:
                    new_sector = (sx, sy + 1)

                if new_sector is not None:
                    self.player.set_sector(new_sector[0], new_sector[1])
                    safe_pos = self.find_safe_position(new_sector)
                    # Оновлюємо обидва rect і hitbox
                    self.player.rect.center = safe_pos
                    self.player.hitbox.center = safe_pos

                #збір квітів 
                collected = self.map_controller.tre_collect_chest(self.player.get_sector(), self.player.rect)
                if collected:
                    self.player.flowers += collected
                    #оновлюємо квест збору квітів
                    self.quest_manager.update_quest("collect_flowers", {
                        "type": "collect",
                        "target": "flower",
                        "progress": collected
                    })

                #оновлюємо ефекти зіллів
                self.player.potion_inventory.update_effects(dt)

            #оновлення камери
            self.camera.update(self.player)

            #малювання сектора
            self.map_controller.draw_sector(self.screen, (self.player.get_sector()))
            #малювання гравця
            self.player.draw(self.screen)
            #малювання феї
            self.fairy.draw(self.screen)
            #малювання верстака
            self.workbench.draw(self.screen)
            #малювання NPC
            self.npcs.draw(self.screen)
            
            #малювання інвентаря зілль
            self.player.potion_inventory.draw(self.screen)
            
            #малювання діалогів
            self.dialogue_system.draw(self.screen)
            
            #малювання інформації про квести
            self.draw_quest_info()

            #малювання кнопки налаштувань
            pygame.draw.rect(self.screen, (200, 200, 200, 80), self.setting_button)

            #малювання підказок для NPC
            for npc in self.npcs:
                npc.draw_interaction_hint(self.screen, self.player)

            #малювання ui квітів 
            flowers_count = self.player.flowers
            if self.ui_frames:
                self.ui_timer += dt
                if self.ui_timer >= self.ui_frame_speed:
                    self.ui_timer -= self.ui_frame_speed
                    self.ui_frame_index = (self.ui_frame_index + 1) % len(self.ui_frames)
                frame = self.ui_frames[self.ui_frame_index]
                padding = 8
                self.screen.blit(frame, (padding, padding))
                font = pygame.font.SysFont(None, 28)
                txt = font.render(str(flowers_count), True, (255, 255, 255))
                self.screen.blit(txt, (padding + frame.get_width() + 8,
                                       padding + (frame.get_height() - txt.get_height()) // 2))
            else:
                font = pygame.font.SysFont(None, 28)
                txt = font.render(str(flowers_count), True, (255, 255, 255))
                self.screen.blit(txt, (8, 8))
                
            #малювання здоров'я
            self.draw_health_bar()

            #підсвічування квітів, якщо активний детектор
            if self.player.potion_inventory.flower_detector_active:
                for chest in self.map_controller.get_chests(self.player.get_sector()):
                    pygame.draw.circle(self.screen, (255, 255, 0), chest['rect'].center, 20, 2)

            #підказка для верстака
            if self.player.rect.colliderect(self.workbench.rect):
                font = pygame.font.SysFont(None, 24)
                hint_txt = font.render("E to open workbench", True, (100, 255, 100)) 
                self.screen.blit(hint_txt, (8, 40))

            #оновлення екрану
            pygame.display.flip()

        pygame.quit()
        
    def draw_health_bar(self):
        #малюємо шкалу здоров'я
        bar_width = 200
        bar_height = 20
        x = 680
        y = const.window_height - bar_height - 10
        
        #фон
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, bar_width, bar_height))
        
        #health fill
        health_width = int((self.player.health / self.player.max_health) * bar_width)
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, health_width, bar_height))
        
        #border
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        #text
        font = pygame.font.SysFont(None, 18)
        text = font.render(f"HP: {self.player.health}/{self.player.max_health}", True, (255, 255, 255))
        self.screen.blit(text, (x + 5, y + 2))
        
    def draw_quest_info(self):
        #малюємо інформацію про квести
        quests_info = self.quest_manager.get_active_quests_info()
        y_offset = 70
        
        font = pygame.font.SysFont(None, 22)
        title = font.render("Active Quests:", True, (200, 200, 100))
        self.screen.blit(title, (8, y_offset))
        y_offset += 25
        
        for quest_info in quests_info:
            name_text = font.render(quest_info["name"], True, (255, 255, 255))
            self.screen.blit(name_text, (8, y_offset))
            y_offset += 20
            
            obj_text = font.render(quest_info["objective"], True, (200, 200, 200))
            self.screen.blit(obj_text, (20, y_offset))
            y_offset += 25