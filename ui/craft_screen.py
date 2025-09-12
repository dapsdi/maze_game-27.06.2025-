import pygame
import settings.constants as const

def show_craft_menu(game):
    # список доступних зіллів для крафтингу
    potions = [
        {"name": "Speed Potion", "cost": const.POTION_COSTS["SPEED"], "effect": "SPEED", "key": "1"},
        {"name": "Invisibility Potion", "cost": const.POTION_COSTS["INVISIBILITY"], "effect": "INVISIBILITY", "key": "2"},
        {"name": "Teleport Potion", "cost": const.POTION_COSTS["TELEPORT"], "effect": "TELEPORT", "key": "3"},
        {"name": "Invulnerability Potion", "cost": const.POTION_COSTS["INVULNERABILITY"], "effect": "INVULNERABILITY", "key": "4"},
        {"name": "Flower Detector Potion", "cost": const.POTION_COSTS["FLOWER_DETECTOR"], "effect": "FLOWER_DETECTOR", "key": "5"}
    ]
    
    # основний цикл меню крафтингу
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_1:
                    craft_potion(game, "SPEED")
                elif event.key == pygame.K_2:
                    craft_potion(game, "INVISIBILITY")
                elif event.key == pygame.K_3:
                    craft_potion(game, "TELEPORT")
                elif event.key == pygame.K_4:
                    craft_potion(game, "INVULNERABILITY")
                elif event.key == pygame.K_5:
                    craft_potion(game, "FLOWER_DETECTOR")
        
        # малюємо меню крафтингу
        game.screen.fill((30, 30, 40))
        font_title = pygame.font.SysFont(None, 48)
        font_item = pygame.font.SysFont(None, 32)
        font_small = pygame.font.SysFont(None, 24)
        
        # заголовок
        title = font_title.render("Crafting Menu", True, const.colors["WHITE"])
        game.screen.blit(title, (game.screen.get_width()//2 - title.get_width()//2, 50))
        
        # інформація про квіти
        flowers_text = font_item.render(f"Flowers: {game.player.flowers}", True, const.colors["YELLOW"])
        game.screen.blit(flowers_text, (game.screen.get_width()//2 - flowers_text.get_width()//2, 120))
        
        # список зіллів
        for i, potion in enumerate(potions):
            y_pos = 180 + i * 60
            color = const.colors["GREEN"] if game.player.flowers >= potion["cost"] else const.colors["RED"]
            
            # назва та вартість
            text = font_item.render(f"{potion['key']}. {potion['name']} - {potion['cost']} flowers", True, color)
            game.screen.blit(text, (game.screen.get_width()//2 - text.get_width()//2, y_pos))
            
            # опис
            desc_text = font_small.render(f"Effect: {get_potion_description(potion['effect'])}", True, const.colors["WHITE"])
            game.screen.blit(desc_text, (game.screen.get_width()//2 - desc_text.get_width()//2, y_pos + 30))
        
        # інструкція
        instruction = font_small.render("Press ESC to return to game", True, const.colors["GRAY"])
        game.screen.blit(instruction, (game.screen.get_width()//2 - instruction.get_width()//2, game.screen.get_height() - 50))
        
        pygame.display.flip()
        game.clock.tick(const.fps)
    
    return True

def get_potion_description(effect):
    # опис ефектів зіллів
    descriptions = {
        "SPEED": "Increases movement speed for 5 seconds",
        "INVISIBILITY": "Makes you invisible and prevents NPC interaction for 7 seconds",
        "TELEPORT": "Teleports you to a random safe location",
        "INVULNERABILITY": "Makes you invulnerable to all damage for 10 seconds",
        "FLOWER_DETECTOR": "Automatically collects all flowers in the room and lasts for 2 minutes"
    }
    return descriptions.get(effect, "Unknown effect")

def craft_potion(game, potion_type):
    # перевіряємо чи достатньо квітів
    cost = const.POTION_COSTS[potion_type]
    if game.player.flowers >= cost:
        game.player.flowers -= cost
        game.player.potion_inventory.inventory[potion_type] += 1
        return True
    return False