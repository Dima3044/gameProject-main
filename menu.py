import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 36)
        self.selected = 0
        self.current_menu = "main"
        self.sounds = {
            'move': pygame.mixer.Sound('sounds/menu/move.wav'),
            'select': pygame.mixer.Sound('sounds/menu/select.wav'),
            'lose': pygame.mixer.Sound('sounds/menu/lose.wav'),
            'victory': pygame.mixer.Sound('sounds/menu/victory.wav')
        }

    def handle_input(self, events):
        """Перемещение по меню, использует приватные методы"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Обработка перемещения
                if event.key in (pygame.K_DOWN, pygame.K_UP):
                    if self.sounds['move']:
                        self.sounds['move'].play()
                    return self._handle_navigation(event.key)

                # Обработка выбора
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if self.sounds['select']:
                        self.sounds['select'].play()
                    return self._handle_selection()

                # Обработка отмены
                elif event.key == pygame.K_ESCAPE:
                    if self.current_menu != "main":
                        if self.sounds['select']:
                            self.sounds['select'].play()
                        return "back"
        return None

    def _handle_navigation(self, key):
        """Логика перемещения стрелками"""
        if self.current_menu == "pause":
            max_items = 3
        elif self.current_menu == "levels":
            max_items = 4
        elif self.current_menu == "defeat":
            max_items = 2
        else:
            max_items = 2

        if key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % max_items
        else:
            self.selected = (self.selected - 1) % max_items

    def _handle_selection(self):
        """Логика выбора пункта"""
        if self.current_menu == "main":
            return ["levels", "quit"][self.selected]
        elif self.current_menu == "levels":
            return ["level1", "level2", "level3", "back"][self.selected]
        elif self.current_menu == "pause":
            return ["continue", "menu", "quit"][self.selected]
        elif self.current_menu == "defeat":
            return ["retry", "menu"][self.selected]
        elif self.current_menu == "victory":
            return "menu"

    def draw(self):
        """Рисует нужное меню"""
        self.screen.fill((30, 30, 40))  # Темно-серый фон

        if self.current_menu == "main":
            title = self.font.render("ЛАБИРИНТ", True, (255, 255, 255))
            options = ["ВЫБРАТЬ УРОВЕНЬ", "ВЫЙТИ ИЗ ИГРЫ"]

        elif self.current_menu == "levels":
            title = self.font.render("ВЫБЕРИТЕ УРОВЕНЬ", True, (255, 255, 255))
            options = ["Уровень 1", "Уровень 2", "Уровень 3", "НАЗАД"]

        elif self.current_menu == "pause":
            title = self.font.render("ПАУЗА", True, (255, 255, 255))
            options = ["ПРОДОЛЖИТЬ", "ВЫЙТИ В МЕНЮ", "ВЫЙТИ ИЗ ИГРЫ"]

        elif self.current_menu == "victory":
            self.sounds['victory'].play()
            title = self.font.render("УРОВЕНЬ ПРОЙДЕН!", True, (0, 255, 0))
            options = ["ВЫЙТИ В МЕНЮ"]

        elif self.current_menu == "defeat":
            self.sounds['lose'].play()
            title = self.font.render("ВЫ ПРОИГРАЛИ!", True, (255, 0, 0))
            options = ["ПОВТОРИТЬ УРОВЕНЬ", "ВЫЙТИ В МЕНЮ"]

        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))
        
        for i, opt in enumerate(options):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(opt, True, color)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, 150 + i*60))
