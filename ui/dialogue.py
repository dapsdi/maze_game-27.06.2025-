import pygame
import settings.constants as const
from ui import colors

class DialogueSystem:
    def __init__(self):
        self.active = False
        self.current_dialogue = []
        self.current_line = 0
        self.font = pygame.font.SysFont(None, 24)
        self.name_font = pygame.font.SysFont(None, 28)
        
    def start_dialogue(self, dialogue_lines):
        self.active = True
        self.current_dialogue = dialogue_lines
        self.current_line = 0
        
    def next_line(self):
        self.current_line += 1
        if self.current_line >= len(self.current_dialogue):
            self.end_dialogue()
            return False
        return True
        
    def end_dialogue(self):
        self.active = False
        self.current_dialogue = []
        self.current_line = 0
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.active:
                self.next_line()
            elif event.key == pygame.K_f and not self.active:
                #передамо обробку F в грі, оскільки тут немає доступу до NPC
                pass
        
    def draw(self, screen):
        if not self.active:
            return
            
        #малюємо діалогове вікно
        dialogue_rect = pygame.Rect(50, screen.get_height() - 150, screen.get_width() - 100, 120)
        pygame.draw.rect(screen, (30, 30, 40), dialogue_rect)
        pygame.draw.rect(screen, colors.colors["WHITE"], dialogue_rect, 2)
        
        if self.current_line < len(self.current_dialogue):
            speaker, text = self.current_dialogue[self.current_line]
            name_text = self.name_font.render(speaker, True, colors.colors["YELLOW"])
            screen.blit(name_text, (dialogue_rect.x + 10, dialogue_rect.y + 10))
            
            text_surface = self.font.render(text, True, colors.colors["WHITE"])
            screen.blit(text_surface, (dialogue_rect.x + 10, dialogue_rect.y + 40))
            
            hint_text = self.font.render("Press SPACE to continue...", True, colors.colors["GRAY"])
            screen.blit(hint_text, (dialogue_rect.x + 10, dialogue_rect.y + 90))