import pygame
from random import choice
import levels

pygame.init()


class Maze():
    def __init__(self, enemy_system):
        self.enemy_system = enemy_system  # Система врагов
        self.enemy_right = pygame.image.load('images/ghost/ghost_right.png').convert_alpha()
        self.enemy_left = pygame.image.load('images/ghost/ghost_left.png').convert_alpha()
        self.keys = []  # Список для ключей и координат
        self.obstacles = [[img.copy(), pos] for img, pos in obstacles]  # Копирование из obstacles
        self.backgrounds = [[img.copy(), pos] for img, pos in backgrounds]  # Копирование из backgrounds
        self.doors = [] 
        self.inventory = []  # Инвентарь для отображения ключей
        self.finish = (800, 1296)  # Метка для отслеживания выхода из лабиринта
        self.MAP = [self.backgrounds, self.obstacles, self.keys, self.doors, self.enemy_system.enemies] 
        # MAP чтобы все элементы окружения были в одном списке

        self.sounds = {
            'pick_up_key': pygame.mixer.Sound('sounds/world/pick_up_key.wav'),  # звук для подбора ключей
            'opened_door': pygame.mixer.Sound('sounds/world/opened_door.wav'),  # звук открывания двери
            'closed_door': pygame.mixer.Sound('sounds/world/closed_door.wav')   # попытка открыть дверь без ключа
        }

    def load_level(self, level_num):
            level_config = levels.LEVEL_CONFIGS.get(level_num, {})
            # Очищаем предыдущие объекты
            self.enemy_system.clear()
            self.keys = []
            self.doors = []

            # Загрузка из конфига
            # Загружаем врагов
            for enemy_data in level_config.get('enemies', []):
                img = pygame.image.load(enemy_data['img']).convert_alpha()
                self.enemy_system.addEnemy(img, enemy_data['pos'])

            # Загружаем ключи
            for key_data in level_config.get('keys', []):
                img = pygame.image.load(key_data['img']).convert_alpha()
                self.keys.append([img, key_data['pos']])

            # Загружаем двери
            for door_data in level_config.get('doors', []):
                img = pygame.image.load(door_data['img']).convert_alpha()
                self.doors.append([img, door_data['pos']])

            # Обновляем карту
            self.MAP = [self.backgrounds, self.obstacles, self.keys,
                self.doors, self.enemy_system.enemies]

    def moveEnemies(self, speed_x=8, speed_y=6):
        for enemy_id, enemy in enumerate(self.enemy_system.enemies):
            enemy_img, enemy_pos = enemy
            enemy_rect = enemy_img.get_rect(topleft=enemy_pos)
            history = self.enemy_system.directions_history[enemy_id]

            # Уменьшаем паузу
            history['pause'] = max(0, history['pause'] - 1)

            # Получаем возможные направления
            directions = self.chooseDirection(enemy_img, enemy_pos)
            if not directions:
                directions = ['right']  # Дефолтное направление если нет вариантов

            # Выбираем новое направление если пауза закончилась
            if history['pause'] <= 0:
                if directions != history['possible_directions']:
                    # Меняем направление только если варианты изменились
                    history['current_direction'] = choice(directions)
                    history['pause'] = 2

            # Обновляем историю
            history['possible_directions'] = directions
            history['last_position'] = enemy_pos

            # Двигаем врага
            direction = history['current_direction']
            new_pos = list(enemy_pos)

            if direction == 'up':
                new_pos[1] -= speed_y
            elif direction == 'down':
                new_pos[1] += speed_y
            elif direction == 'left':
                enemy[0] = self.enemy_left
                new_pos[0] -= speed_x
            elif direction == 'right':
                enemy[0] = self.enemy_right
                new_pos[0] += speed_x

            # Обновляем позицию
            enemy[1] = tuple(new_pos)

    def chooseDirection(self, enemy, coord, speed_x=8, speed_y=6):
        directions = []  # Сначала пусто
        rect = enemy.get_rect(topleft=coord)

        # По очереди проверяем, есть у врага место со всех сторон
        rect[0] += speed_x
        if not self.check_intersection(rect, is_player=False):
            directions.append('right')
        rect[0] -= speed_x * 2
        if not self.check_intersection(rect, is_player=False):
            directions.append('left')
        rect[0] += speed_x
        rect[1] -= speed_y
        if not self.check_intersection(rect, is_player=False):
            directions.append('up')
        rect[1] += speed_x * 2
        if not self.check_intersection(rect, is_player=False):
            directions.append('down')
        rect[1] -= speed_y

        # Возвращаем список возможных направлений
        return directions if directions else ['right']

    def drawMap(self, screen):  
        for group in self.MAP:  # Отрисовка окружения
            for obs, coord in group:
                screen.blit(obs, coord)
        for item, coord in self.inventory:  # Отрисовка инвентаря
            screen.blit(item, coord)

    def moveMap(self, speed_x=0, speed_y=0):  # Перемещение всех объектов в MAP
        for group in self.MAP:
            for obj in group:
                x, y = obj[1]
                if speed_x != 0:
                    x += speed_x
                if speed_y != 0:
                    y += speed_y
                obj[1] = (x, y)

        x, y = self.finish  # И финиша
        if speed_x != 0:
            x += speed_x
        if speed_y != 0:
            y += speed_y
        self.finish = (x, y)

    def check_victory(self):
        # Проверка, вышел ли игрок из лабиринта
        if self.finish[1] <= 240:
            return True
        return False

    def check_defeat(self, player_rect):  # Проигрыш при контакте с врагом
        for enemy_img, enemy_pos in self.enemy_system.enemies:
            enemy_rect = enemy_img.get_rect(topleft=enemy_pos)
            if player_rect.colliderect(enemy_rect):
                return True
        return False

    def check_intersection(self, rect, is_player=True):
        obstacles_rect_list = []
        if is_player:  # Проверка что двигается игрок, чтобы враги не воровали ключи, например
            keys_rect_list = [key.get_rect(topleft=coord) for key, coord in self.keys]
            for index, key_rect in enumerate(keys_rect_list):
                if key_rect.colliderect(rect):
                    self.keys.pop(index)
                    key_x = len(self.inventory) * 32  # 32 пикселя - размер ключа
                    self.sounds['pick_up_key'].play()  # звук для ключа
                    self.inventory.append([key, (key_x, 0)])  # добавление в инвентарь

            doors_rect_list = [door.get_rect(topleft=coord) for door, coord in self.doors]
            for index, door_rect in enumerate(doors_rect_list):
                if door_rect.colliderect(rect):
                    if not self.inventory:  # если нет ключа, но есть контакт с дверью
                        self.sounds['closed_door'].play()
                        return True
                    else:  # если ключ есть
                        self.doors.pop(index)  # Удаляем конкретную дверь, с которой столкнулись
                        self.inventory.pop()
                        self.sounds['opened_door'].play()
                        return True
        # Проверка на столкновение со стеной, общее для врагов и игрока
        obstacles_rect_list = [obstacle.get_rect(topleft=coord) for obstacle, coord in self.obstacles]
        for obs_rect in obstacles_rect_list:
            if obs_rect.colliderect(rect):
                return True
        return False


class Enemy():
    def __init__(self):
        self.enemies = []  # Список врагов вида [[img, pos], ...]
        self.directions_history = {}  # Словарь истории направлений

    def addEnemy(self, img, coord):
        enemy_id = len(self.enemies)  # ID равен текущему количеству врагов
        self.enemies.append([img, coord])
        # Инициализируем запись для этого врага
        self.directions_history[enemy_id] = {
            'possible_directions': [],
            'current_direction': 'right',
            'pause': 2,
            'last_position': coord
        }

    def clear(self):
        self.enemies.clear()
        self.directions_history.clear()


key = pygame.image.load('images/key.png')
background = pygame.image.load('images/background.png')
screen = pygame.display.set_mode((300, 300), pygame.FULLSCREEN)
obstacles = [
    [pygame.image.load('images/obstacles/obstacle1.png').convert_alpha(), (0, 0)],
    [pygame.image.load('images/obstacles/obstacle2.png').convert_alpha(), (32, 0)],
    [pygame.image.load('images/obstacles/obstacle3.png').convert_alpha(), (832, 0)],
    [pygame.image.load('images/obstacles/obstacle4.png').convert_alpha(), (32, 1248)],
    [pygame.image.load('images/obstacles/obstacle5.png').convert_alpha(), (256, 48)],
    [pygame.image.load('images/obstacles/obstacle6.png').convert_alpha(), (288, 96)],
    [pygame.image.load('images/obstacles/obstacle7.png').convert_alpha(), (512, 48)],
    [pygame.image.load('images/obstacles/obstacle8.png').convert_alpha(), (576, 96)],
    [pygame.image.load('images/obstacles/obstacle9.png').convert_alpha(), (32, 384)],
    [pygame.image.load('images/obstacles/obstacle10.png').convert_alpha(), (64, 480)],
    [pygame.image.load('images/obstacles/obstacle11.png').convert_alpha(), (128, 528)],
    [pygame.image.load('images/obstacles/obstacle12.png').convert_alpha(), (64, 576)],
    [pygame.image.load('images/obstacles/obstacle13.png').convert_alpha(), (64, 624)],
    [pygame.image.load('images/obstacles/obstacle14.png').convert_alpha(), (32, 672)],
    [pygame.image.load('images/obstacles/obstacle15.png').convert_alpha(), (32, 864)],
    [pygame.image.load('images/obstacles/obstacle16.png').convert_alpha(), (32, 960)],
    [pygame.image.load('images/obstacles/obstacle17.png').convert_alpha(), (64, 1056)],
    [pygame.image.load('images/obstacles/obstacle18.png').convert_alpha(), (64, 1104)],
    [pygame.image.load('images/obstacles/obstacle19.png').convert_alpha(), (96, 1152)],
    [pygame.image.load('images/obstacles/obstacle20.png').convert_alpha(), (192, 1200)],
    [pygame.image.load('images/obstacles/obstacle21.png').convert_alpha(), (320, 192)],
    [pygame.image.load('images/obstacles/obstacle22.png').convert_alpha(), (256, 288)],
    [pygame.image.load('images/obstacles/obstacle23.png').convert_alpha(), (256, 336)],
    [pygame.image.load('images/obstacles/obstacle24.png').convert_alpha(), (128, 384)],
    [pygame.image.load('images/obstacles/obstacle25.png').convert_alpha(), (384, 192)],
    [pygame.image.load('images/obstacles/obstacle26.png').convert_alpha(), (288, 384)],
    [pygame.image.load('images/obstacles/obstacle27.png').convert_alpha(), (192, 480)],
    [pygame.image.load('images/obstacles/obstacle28.png').convert_alpha(), (128, 672)],
    [pygame.image.load('images/obstacles/obstacle29.png').convert_alpha(), (128, 720)],
    [pygame.image.load('images/obstacles/obstacle30.png').convert_alpha(), (64, 768)],
    [pygame.image.load('images/obstacles/obstacle31.png').convert_alpha(), (256, 1152)],
    [pygame.image.load('images/obstacles/obstacle32.png').convert_alpha(), (192, 1008)],
    [pygame.image.load('images/obstacles/obstacle33.png').convert_alpha(), (224, 1056)],
    [pygame.image.load('images/obstacles/obstacle34.png').convert_alpha(), (320, 1104)],
    [pygame.image.load('images/obstacles/obstacle35.png').convert_alpha(), (384, 1152)],
    [pygame.image.load('images/obstacles/obstacle36.png').convert_alpha(), (416, 1152)],
    [pygame.image.load('images/obstacles/obstacle37.png').convert_alpha(), (704, 1152)],
    [pygame.image.load('images/obstacles/obstacle38.png').convert_alpha(), (736, 1152)],
    [pygame.image.load('images/obstacles/obstacle39.png').convert_alpha(), (704, 1056)],
    [pygame.image.load('images/obstacles/obstacle40.png').convert_alpha(), (640, 960)],
    [pygame.image.load('images/obstacles/obstacle41.png').convert_alpha(), (672, 960)],
    [pygame.image.load('images/obstacles/obstacle42.png').convert_alpha(), (768, 768)],
    [pygame.image.load('images/obstacles/obstacle43.png').convert_alpha(), (800, 768)],
    [pygame.image.load('images/obstacles/obstacle44.png').convert_alpha(), (576, 1056)],
    [pygame.image.load('images/obstacles/obstacle45.png').convert_alpha(), (768, 144)],
    [pygame.image.load('images/obstacles/obstacle46.png').convert_alpha(), (800, 288)],
    [pygame.image.load('images/obstacles/obstacle47.png').convert_alpha(), (640, 144)],
    [pygame.image.load('images/obstacles/obstacle48.png').convert_alpha(), (448, 144)],
    [pygame.image.load('images/obstacles/obstacle49.png').convert_alpha(), (480, 192)],
    [pygame.image.load('images/obstacles/obstacle50.png').convert_alpha(), (704, 192)],
    [pygame.image.load('images/obstacles/obstacle51.png').convert_alpha(), (736, 384)],
    [pygame.image.load('images/obstacles/obstacle52.png').convert_alpha(), (512, 288)],
    [pygame.image.load('images/obstacles/obstacle53.png').convert_alpha(), (576, 240)],
    [pygame.image.load('images/obstacles/obstacle54.png').convert_alpha(), (448, 288)],
    [pygame.image.load('images/obstacles/obstacle55.png').convert_alpha(), (480, 384)],
    [pygame.image.load('images/obstacles/obstacle56.png').convert_alpha(), (512, 336)],
    [pygame.image.load('images/obstacles/obstacle57.png').convert_alpha(), (320, 480)],
    [pygame.image.load('images/obstacles/obstacle58.png').convert_alpha(), (320, 528)],
    [pygame.image.load('images/obstacles/obstacle59.png').convert_alpha(), (352, 672)],
    [pygame.image.load('images/obstacles/obstacle60.png').convert_alpha(), (384, 576)],
    [pygame.image.load('images/obstacles/obstacle61.png').convert_alpha(), (448, 720)],
    [pygame.image.load('images/obstacles/obstacle62.png').convert_alpha(), (192, 768)],
    [pygame.image.load('images/obstacles/obstacle63.png').convert_alpha(), (160, 864)],
    [pygame.image.load('images/obstacles/obstacle64.png').convert_alpha(), (384, 816)],
    [pygame.image.load('images/obstacles/obstacle65.png').convert_alpha(), (256, 912)],
    [pygame.image.load('images/obstacles/obstacle66.png').convert_alpha(), (288, 960)],
    [pygame.image.load('images/obstacles/obstacle67.png').convert_alpha(), (512, 480)],
    [pygame.image.load('images/obstacles/obstacle68.png').convert_alpha(), (384, 960)],
    [pygame.image.load('images/obstacles/obstacle69.png').convert_alpha(), (416, 960)],
    [pygame.image.load('images/obstacles/obstacle70.png').convert_alpha(), (448, 1008)],
    [pygame.image.load('images/obstacles/obstacle71.png').convert_alpha(), (480, 1056)],
    [pygame.image.load('images/obstacles/obstacle72.png').convert_alpha(), (512, 768)],
    [pygame.image.load('images/obstacles/obstacle73.png').convert_alpha(), (576, 864)],
    [pygame.image.load('images/obstacles/obstacle74.png').convert_alpha(), (608, 864)],
    [pygame.image.load('images/obstacles/obstacle75.png').convert_alpha(), (544, 768)],
    [pygame.image.load('images/obstacles/obstacle76.png').convert_alpha(), (576, 576)],
    [pygame.image.load('images/obstacles/obstacle77.png').convert_alpha(), (544, 480)],
    [pygame.image.load('images/obstacles/obstacle78.png').convert_alpha(), (576, 384)],
    [pygame.image.load('images/obstacles/obstacle79.png').convert_alpha(), (608, 384)],
    [pygame.image.load('images/obstacles/obstacle80.png').convert_alpha(), (640, 432)],
    [pygame.image.load('images/obstacles/obstacle81.png').convert_alpha(), (672, 480)],
    [pygame.image.load('images/obstacles/obstacle82.png').convert_alpha(), (768, 480)],
    [pygame.image.load('images/obstacles/obstacle83.png').convert_alpha(), (640, 576)],
    [pygame.image.load('images/obstacles/obstacle84.png').convert_alpha(), (672, 576)],
    [pygame.image.load('images/obstacles/obstacle85.png').convert_alpha(), (768, 624)],
    [pygame.image.load('images/obstacles/obstacle86.png').convert_alpha(), (704, 672)],
    [pygame.image.load('images/obstacles/obstacle87.png').convert_alpha(), (704, 720)],
]
backgrounds = [
    [background, (0, 0)],
    [background, (-864, 0)],
    [background, (-864, -1296)],
    [background, (-864, 1296)],
    [background, (0, 1296)],
    [background, (0, -1296)],
    [background, (864, 1296)],
    [background, (864, -1296)],
    [background, (864, 0)]
]
