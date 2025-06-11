import pygame
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font('fonts/Roboto_Condensed-Black.ttf', 30)
        self.selected = 0
        self.menu_active = True
        self.paused = False
        
    def draw_main_menu(self):
        self.screen.fill((30, 30, 40))
        title = self.font.render("ЛАБИРИНТ", True, (255, 255, 255))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        options = ["ВЫБРАТЬ УРОВЕНЬ", "ВЫЙТИ ИЗ ИГРЫ"]
        for i, opt in enumerate(options):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(opt, True, color)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, 150 + i*60))
    
    def draw_level_select(self):
        self.screen.fill((30, 30, 40))
        title = self.font.render("ВЫБЕРИТЕ УРОВЕНЬ", True, (255, 255, 255))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        levels = ["Уровень 1", "Уровень 2", "Уровень 3", "НАЗАД"]
        for i, level in enumerate(levels):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(level, True, color)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, 150 + i*50))
    
    def draw_pause_menu(self):
        # Полупрозрачный фон
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        
        options = ["ПРОДОЛЖИТЬ", "ВЫЙТИ В МЕНЮ", "ВЫЙТИ ИЗ ИГРЫ"]
        for i, opt in enumerate(options):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(opt, True, color)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, 150 + i*60))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % (3 if self.paused or self.menu_active else 4)
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % (3 if self.paused or self.menu_active else 4)
                elif event.key == pygame.K_RETURN:
                    return self.get_selected_action()
                elif event.key == pygame.K_ESCAPE:
                    if self.paused:
                        return "continue"
        return None
    
    def get_selected_action(self):
        if self.paused:
            return ["continue", "main_menu", "quit"][self.selected]
        elif not self.menu_active:  # Выбор уровня
            return ["level1", "level2", "level3", "back"][self.selected]
        else:  # Главное меню
            return ["level_select", "quit"][self.selected]