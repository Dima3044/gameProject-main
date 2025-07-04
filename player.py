import pygame

pygame.init()
screen = pygame.display.set_mode((300, 300), pygame.FULLSCREEN)


class Player():
    def __init__(self):
        self.player_front = pygame.image.load('images/player_front/front1.png').convert_alpha()  # Лицеваая сторона
        self.player_back = pygame.image.load('images/player_back/back1.png').convert_alpha()  # Спина
        self.player_rect = self.player_front.get_rect(topleft=(288, 240))  # Координаты спавна
        self.anim_count = 0  # Для анимации спрайта
        self.player_orientation = 'front'  # Изначальное положение
        self.is_moving = False  # Двигается игрок или нет
        self.player_speed_x = 16
        self.player_speed_y = 12
        self.player_hit_box = pygame.image.load('images/player_front/player_hit_box.png').convert_alpha()
        self.walk_sound = pygame.mixer.Sound('sounds/player/walk_sound.wav')
        self.step_delay = 200  # Чтобы при ходьбе звук не накладывался
        self.last_step_time = 0  # Счётчик от последнего шага

        self.player_front_walking = [
            pygame.image.load('images/player_front/front2.png').convert_alpha(),
            pygame.image.load('images/player_front/front3.png').convert_alpha(),
        ]

        self.player_back_walking = [
            pygame.image.load('images/player_back/back2.png').convert_alpha(),
            pygame.image.load('images/player_back/back3.png').convert_alpha(),
        ]

    def move(self, maze, keys):
        """Отвечает за перемещение игрока"""
        current_time = pygame.time.get_ticks()
        # Проверка нажатия на стрелочики
        if keys[pygame.K_LEFT]:
            maze.moveMap(speed_x=self.player_speed_x)
            if maze.check_intersection(self.player_rect):
                maze.moveMap(speed_x=-self.player_speed_x)
            self.is_moving = True

        elif keys[pygame.K_RIGHT]:
            maze.moveMap(speed_x=-self.player_speed_x)
            if maze.check_intersection(self.player_rect):
                maze.moveMap(speed_x=self.player_speed_x)
            self.is_moving = True

        elif keys[pygame.K_UP]:
            self.player_orientation = 'back'
            maze.moveMap(speed_y=self.player_speed_y)
            if maze.check_intersection(self.player_rect):
                maze.moveMap(speed_y=-self.player_speed_y)
            self.is_moving = True

        elif keys[pygame.K_DOWN]:
            self.player_orientation = 'front'
            maze.moveMap(speed_y=-self.player_speed_y)
            if maze.check_intersection(self.player_rect):
                maze.moveMap(speed_y=self.player_speed_y)
            self.is_moving = True

        else:  # Если стрелочки не нажаты
            self.is_moving = False

        if self.is_moving:  # Если игрок двигается, то проигрываем звук с задержкой
            if current_time - self.last_step_time > self.step_delay:
                            self.walk_sound.stop()
                            self.walk_sound.play()
                            self.last_step_time = current_time

            if self.player_orientation == 'front':
                screen.blit(self.player_front_walking[self.anim_count], self.player_rect)
            else:
                screen.blit(self.player_back_walking[self.anim_count], self.player_rect)
        else:
            if self.player_orientation == 'front':
                screen.blit(self.player_front, self.player_rect)
            else:
                screen.blit(self.player_back, self.player_rect)
        # Для анимации
        self.anim_count += 1
        if self.anim_count >= 2:
            self.anim_count = 0
