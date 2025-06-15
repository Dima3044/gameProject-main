import pygame
import sys


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 36)
        self.selected = 0
        self.current_menu = "main"  # "main", "levels", "pause", "victory", "defeat"
        
    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.current_menu == "pause":
                        self.selected = (self.selected + 1) % 3
                    elif self.current_menu == "levels":
                        self.selected = (self.selected + 1) % 4
                    elif self.current_menu == "defeat":
                        self.selected = (self.selected + 1) % 2
                    else:
                        self.selected = (self.selected + 1) % 2
                        
                elif event.key == pygame.K_UP:
                    if self.current_menu == "pause":
                        self.selected = (self.selected - 1) % 3
                    elif self.current_menu == "levels":
                        self.selected = (self.selected - 1) % 4
                    elif self.current_menu == "defeat":
                        self.selected = (self.selected - 1) % 2
                    else:
                        self.selected = (self.selected - 1) % 2
                        
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if self.current_menu == "main":
                        return ["levels", "quit"][self.selected]
                    elif self.current_menu == "levels":
                        return ["level1", "level2", "level3", "back"][self.selected]
                    elif self.current_menu == "pause":
                        return ["continue", "menu", "quit"][self.selected]
                    elif self.current_menu == "victory":
                        return "menu"
                    elif self.current_menu == "defeat":
                        return ["retry", "menu"][self.selected]
                        
                elif event.key == pygame.K_ESCAPE:
                    if self.current_menu == "levels":
                        return "back"
                    elif self.current_menu == "pause":
                        return "continue"
        return None

    def draw(self):
        self.screen.fill((30, 30, 40))  # Темно-серый фон
        
        if self.current_menu == "main":
            self.draw_main_menu()
        elif self.current_menu == "levels":
            self.draw_level_select()
        elif self.current_menu == "pause":
            self.draw_pause_menu()
        elif self.current_menu == "victory":
            self.draw_victory_screen()
        elif self.current_menu == "defeat":
            self.draw_defeat_screen()

    def draw_main_menu(self):
        title = self.font.render("ЛАБИРИНТ", True, (255, 255, 255))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        options = ["ВЫБРАТЬ УРОВЕНЬ", "ВЫЙТИ ИЗ ИГРЫ"]
        for i, opt in enumerate(options):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(opt, True, color)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, 150 + i*60))

    def draw_level_select(self):
        title = self.font.render("ВЫБЕРИТЕ УРОВЕНЬ", True, (255, 255, 255))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        levels = ["Уровень 1", "Уровень 2", "Уровень 3", "НАЗАД"]
        for i, level in enumerate(levels):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(level, True, color)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, 150 + i*50))

    def draw_pause_menu(self):
        options = ["ПРОДОЛЖИТЬ", "ВЫЙТИ В МЕНЮ", "ВЫЙТИ ИЗ ИГРЫ"]
        for i, opt in enumerate(options):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(opt, True, color)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, 150 + i*60))

    def draw_victory_screen(self):
        title = self.font.render("УРОВЕНЬ ПРОЙДЕН!", True, (0, 255, 0))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        option = self.font.render("ВЫЙТИ В МЕНЮ", True, 
                                (255, 215, 0) if self.selected == 0 else (255, 255, 255))
        self.screen.blit(option, (self.width//2 - option.get_width()//2, 150))

    def draw_defeat_screen(self):
        title = self.font.render("ВЫ ПРОИГРАЛИ!", True, (255, 0, 0))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        options = ["ПОВТОРИТЬ УРОВЕНЬ", "ВЫЙТИ В МЕНЮ"]
        for i, opt in enumerate(options):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(opt, True, color)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, 150 + i*60))