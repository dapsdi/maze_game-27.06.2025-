import pygame
import math

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, npc_type="villager", dialogues=[]):
        super().__init__()
        self.x = x
        self.y = y
        self.type = npc_type
        self.dialogues = dialogues  #список діалогів для цього NPC
        
        #створюємо простий спрайт
        self.image = pygame.Surface((32, 32))
        if npc_type == "villager":
            self.image.fill((0, 255, 0))  #зелений для мирних NPC
        elif npc_type == "merchant":
            self.image.fill((255, 165, 0))  #помаранчевий для торговців
        else:
            self.image.fill((200, 200, 200))  #сірий для інших типів
            
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.interaction_range = 100  #дистанція для взаємодії

    def can_interact(self, player):
        #перевіряємо чи гравець достатньо близько для взаємодії
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.sqrt(dx*dx + dy*dy)
        return dist <= self.interaction_range

    def get_dialogues(self):
        #повертаємо діалоги для цього NPC
        return self.dialogues

    def draw_interaction_hint(self, screen, player):
        #малюємо підказку для взаємодії, якщо гравець поруч
        if self.can_interact(player):
            font = pygame.font.SysFont(None, 20)
            text = font.render("Press F to talk", True, (255, 255, 255))
            screen.blit(text, (self.rect.x, self.rect.y - 20))