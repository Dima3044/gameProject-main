from enviroment import Maze, Enemy
import pygame
from player import Player
from menu import Menu

pygame.init()
clock = pygame.time.Clock()
info = pygame.display.Info()
ambient = pygame.mixer.Sound('sounds/world/ambient.mp3')
pygame.display.set_caption("Лабиринт")


def load_level(level_num):
    """Загрузка выбранного уровня"""
    enemy_system = Enemy()
    maze = Maze(enemy_system)
    maze.load_level(level_num)
    return maze, Player(), enemy_system


def game_loop(maze, player_obj, enemy_system, screen):
    """Основной цикл с обработкой ситуации"""
    running = True
    while running:
        # Очистка экрана
        screen.fill((0, 0, 0))

        if maze.check_victory():
            return "level_complete"
        if maze.check_defeat(player_obj.player_rect):
            return "game_over"

        # Игровая логика
        maze.moveEnemies()
        maze.drawMap(screen)

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
    pygame.init()
    screen = pygame.display.set_mode((300, 300), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    menu = Menu(screen)

    game_state = {
        "current": "menu",
        "level": 1,
        "objects": None
    }

    running = True
    while running:
        events = pygame.event.get()

        # Обработка выхода
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Обработка ввода
        action = None
        if game_state["current"] != "game":
            action = menu.handle_input(events)

        # Обработка действий
        if action == "levels":
            menu.current_menu = "levels"
        elif action == "back":
            menu.current_menu = "main"
            menu.selected = 0
        elif action in ["level1", "level2", "level3"]:
            game_state["level"] = int(action[-1])
            game_state["objects"] = load_level(game_state["level"])
            game_state["current"] = "game"
        elif action == "continue":
            game_state["current"] = "game"
        elif action == "menu":
            game_state["current"] = "menu"
            menu.current_menu = "main"
        elif action == "retry":
            game_state["objects"] = load_level(game_state["level"])
            game_state["current"] = "game"
        elif action == "quit":
            running = False

        # Игровая логика
        if game_state["current"] == "game":
            ambient.play(loops=-1)
            result = game_loop(*game_state["objects"], screen)
            if result == "level_complete":
                game_state["current"] = "victory"
                menu.current_menu = "victory"
            elif result == "game_over":
                game_state["current"] = "defeat"
                menu.current_menu = "defeat"
            elif result == "pause":
                game_state["current"] = "pause"
                menu.current_menu = "pause"
        else:
            ambient.stop()

        # Отрисовка
        screen.fill((0, 0, 0))
        if game_state["current"] == "game":
            pass
        else:
            menu.draw()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
