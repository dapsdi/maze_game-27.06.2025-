import json
import os
import pygame
import settings.constants as const

class SaveLoadSystem:
    def __init__(self):
        self.save_dir = "saves"
        os.makedirs(self.save_dir, exist_ok=True)
    
    def save_game(self, player, map_controller, filename="save.json"):
        #збираємо всі дані для збереження
        save_data = {
            "player": {
                "sector": player.sector,
                "position": (player.rect.x, player.rect.y),
                "flowers": player.flowers,
                "health": player.health,
                "inventory": player.potion_inventory.inventory,
                "noclip": player.noclip
            },
            "map": {
                "visited_sectors": self.get_visited_sectors(map_controller),
                "collected_chests": self.get_collected_chests(map_controller)
            }
        }
        
        #зберігаємо у файл
        with open(os.path.join(self.save_dir, filename), 'w') as f:
            json.dump(save_data, f, indent=4)
    
    def load_game(self, player, map_controller, filename="save.json"):
        try:
            with open(os.path.join(self.save_dir, filename), 'r') as f:
                save_data = json.load(f)
            
            #відновлюємо стан гравця
            player.sector = tuple(save_data["player"]["sector"])
            player.rect.x, player.rect.y = save_data["player"]["position"]
            player.flowers = save_data["player"]["flowers"]
            player.health = save_data["player"]["health"]
            player.potion_inventory.inventory = save_data["player"]["inventory"]
            player.noclip = save_data["player"]["noclip"]
            
            #відновлюємо стан карти
            self.restore_map_state(map_controller, save_data["map"])
            
            return True
        except:
            return False
    
    def get_visited_sectors(self, map_controller):
        #збираємо відвідані сектори
        visited = []
        for x in range(const.map_width):
            for y in range(const.map_height):
                if map_controller.grid[x][y].get('visited', False):
                    visited.append((x, y))
        return visited
    
    def get_collected_chests(self, map_controller):
        #збираємо інформацію про зібрані скрині
        collected = {}
        for x in range(const.map_width):
            for y in range(const.map_height):
                original_count = const.max_chests_per_sector
                current_count = len(map_controller.grid[x][y]['chests'])
                if current_count < original_count:
                    collected[f"{x},{y}"] = original_count - current_count
        return collected
    
    def restore_map_state(self, map_controller, map_data):
        #відновлюємо стан карти
        for sector in map_data["visited_sectors"]:
            x, y = sector
            map_controller.grid[x][y]['visited'] = True
        
        for sector_key, collected_count in map_data["collected_chests"].items():
            x, y = map(int, sector_key.split(','))
            #відновлюємо кількість скринь, які були зібрані
            map_controller.grid[x][y]['chests'] = map_controller.grid[x][y]['chests'][:-collected_count]