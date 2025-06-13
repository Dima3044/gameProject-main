from enviroment import Maze, Enemy
import pygame
from player import Player
from menu import Menu

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))  # Увеличим размер окна
pygame.display.set_caption("Лабиринт")

# Загрузка ресурсов
def load_level(level_num):
    # Создаем новую систему врагов
    enemy_system = Enemy()
    
    # Создаем лабиринт
    maze = Maze(enemy_system)
    
    # Настраиваем уровень
    if level_num == 1:
        zombie_img = pygame.image.load('images/zombie.png').convert_alpha()
        enemy_system.addEnemy(zombie_img, (352, 1008))  # Теперь правильно инициализирует directions_history
    elif level_num == 2:
        pass
    elif level_num == 3:
        pass
    return maze, Player(), enemy_system

def game_loop(maze, player_obj, enemy_system, screen):
    running = True
    while running:
        # Очистка экрана
        screen.fill((0, 0, 0))
        
        # Игровая логика
        maze.moveEnemies()
        maze.drawMap(screen)
        maze.drawInventory(screen)
        
        keys = pygame.key.get_pressed()
        player_obj.move(maze, keys)
        
        pygame.display.update()
        clock.tick(15)
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "pause"
    
    return "main_menu"

def main():
    menu = Menu(screen)
    current_screen = "main_menu"  # main_menu/level_select/game/pause
    level = 1
    
    while True:
        if current_screen == "main_menu":
            menu.menu_active = True
            menu.paused = False
            menu.draw_main_menu()
            action = menu.handle_events()
            
            if action == "level_select":
                current_screen = "level_select"
            elif action == "quit":
                pygame.quit()
                return
                
        elif current_screen == "level_select":
            menu.menu_active = False
            menu.draw_level_select()
            action = menu.handle_events()
            
            if action in ["level1", "level2", "level3"]:
                level = int(action[-1])
                current_screen = "game"
            elif action == "back":
                current_screen = "main_menu"
                
        elif current_screen == "game":
            # Загружаем уровень с нужными параметрами
            maze, player_obj, enemy_system = load_level(level)
            
            # Передаем все 4 аргумента
            result = game_loop(maze, player_obj, enemy_system, screen)
            
            if result == "pause":
                current_screen = "pause"
            elif result == "quit":
                pygame.quit()
                return
            elif result == "main_menu":
                current_screen = "main_menu"
                
        elif current_screen == "pause":
            menu.paused = True
            menu.draw_pause_menu()
            action = menu.handle_events()
            
            if action == "continue":
                current_screen = "game"
            elif action == "main_menu":
                current_screen = "main_menu"
            elif action == "quit":
                pygame.quit()
                return
                
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()