import pygame
import sys


def check_enemy_collision(player_obj, enemy_system):
    """Проверка столкновения игрока с врагами"""
    player_rect = player_obj.player_rect
    for enemy in enemy_system.enemies:
        enemy_img, enemy_pos = enemy
        enemy_rect = enemy_img.get_rect(topleft=enemy_pos)
        if player_rect.colliderect(enemy_rect):
            return True
    return False


def draw_pause_menu(screen):
    """Отрисовка меню паузы"""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 50)
    text = font.render("ПАУЗА", True, (255, 255, 255))
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 150))

    font = pygame.font.Font(None, 36)
    continue_text = font.render("Продолжить (ESC)", True, (255, 255, 255))
    menu_text = font.render("Выйти в меню (M)", True, (255, 255, 255))

    screen.blit(continue_text, (screen.get_width()//2 - continue_text.get_width()//2, 250))
    screen.blit(menu_text, (screen.get_width()//2 - menu_text.get_width()//2, 300))


def draw_victory_screen(screen):
    """Отрисовка экрана победы"""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 50, 0, 200))
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 50)
    text = font.render("ПОБЕДА!", True, (255, 215, 0))
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 150))

    font = pygame.font.Font(None, 36)
    hint = font.render("Нажмите Enter для выхода в меню", True, (255, 255, 255))
    screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, 250))


def draw_defeat_screen(screen):
    """Отрисовка экрана поражения"""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((50, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 50)
    text = font.render("ПОРАЖЕНИЕ", True, (255, 0, 0))
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 150))

    font = pygame.font.Font(None, 36)
    restart_text = font.render("Заново (R)", True, (255, 255, 255))
    menu_text = font.render("Выйти в меню (M)", True, (255, 255, 255))

    screen.blit(restart_text, (screen.get_width()//2 - restart_text.get_width()//2, 250))
    screen.blit(menu_text, (screen.get_width()//2 - menu_text.get_width()//2, 300))


def handle_endgame_events():
    """Обработка событий на экранах победы/поражения"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Рестарт
                return "restart"
            if event.key in (pygame.K_RETURN, pygame.K_m):  # В меню
                return "main_menu"
            if event.key == pygame.K_ESCAPE:  # Выход
                pygame.quit()
                sys.exit()
    return None
