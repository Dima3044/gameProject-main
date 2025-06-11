import pygame
from random import choice

pygame.init()


class Maze():
    def __init__(self):
        self.keys = keys
        self.obstacles = obstacles
        self.backgrounds = backgrounds
        self.doors = doors
        self.inventory = []
        self.MAP = [self.backgrounds, self.obstacles, self.keys, self.doors, enemies]


    def load_level(self, level_num):
        if level_num == 1:
            self.doors = [[door_ver, (768, 528)]]
            self.keys = [[key, (480, 1008)], [key, (96, 96)]]
        elif level_num == 2:
            # Конфигурация для уровня 2
            pass
        elif level_num == 3:
            # Конфигурация для уровня 3
            pass
    def moveEnemies(self, speed_x=8, speed_y=6):
        id = 0
        for enemy in enemies:
            enemy_rect = enemy[0].get_rect(topleft=enemy[1])
            x, y = enemy[1]
            direction = directions_history[id][1]
            pause = directions_history[id][2]
            pause -= 1
            directions = self.chooseDirection(enemy[0], enemy[1])
            if pause <= 0:
                pause = 2
                if directions == directions_history[id][0] and (x, y) != directions_history[id][3]:
                    direction = directions_history[id][1]
                else:
                    up_or_down = []
                    left_or_right = []
                    if direction == 'right' or direction == 'left':
                        if 'up' in directions:
                            up_or_down.append('up')
                        if 'down' in directions:
                            up_or_down.append('down')

                    elif direction == 'up' or direction == 'down':
                        if 'right' in directions:
                            left_or_right.append('right')
                        if 'left' in directions:
                            left_or_right.append('left')

                    if up_or_down:
                        direction = choice(up_or_down)
                    elif left_or_right:
                        direction = choice(left_or_right)
                    else:
                        direction = choice(directions)
            else:
                direction = directions_history[id][1]
            directions_history[id] = [directions, direction, pause, (x, y)]
            if direction == 'up':
                enemy_rect[1] -= speed_y
                if not self.checkIntersection(enemy_rect, is_player=False):
                    enemy_rect[1] += speed_y
                    y -= speed_y

            elif direction == 'down':
                enemy_rect[1] += speed_y
                if not self.checkIntersection(enemy_rect, is_player=False):
                    enemy_rect[1] -= speed_y
                    y += speed_y

            elif direction == 'right':
                enemy_rect[0] += speed_x
                if not self.checkIntersection(enemy_rect, is_player=False):
                    enemy_rect[0] -= speed_x
                    x += speed_x

            elif direction == 'left':
                enemy_rect[0] -= speed_x
                if not self.checkIntersection(enemy_rect, is_player=False):
                    enemy_rect[0] += speed_x
                    x -= speed_x
            enemy[1] = (x, y)
            id += 1

    def chooseDirection(self, enemy, coord, speed_x=8, speed_y=6):
        directions = []
        rect = enemy.get_rect(topleft=coord)
        rect[0] += speed_x
        if not self.checkIntersection(rect, is_player=False):
            directions.append('right')
        rect[0] -= speed_x * 2
        if not self.checkIntersection(rect, is_player=False):
            directions.append('left')
        rect[0] += speed_x
        rect[1] -= speed_y
        if not self.checkIntersection(rect, is_player=False):
            directions.append('up')
        rect[1] += speed_x * 2
        if not self.checkIntersection(rect, is_player=False):
            directions.append('down')
        rect[1] -= speed_y

        return directions

    def drawMap(self, screen):
        for group in self.MAP:
            for obs, coord in group:
                screen.blit(obs, coord)

    def drawInventory(self, screen):
        for item, coord in self.inventory:
            screen.blit(item, coord)

    def moveMap(self, speed_x=0, speed_y=0):
        for group in self.MAP:
            for obj in group:
                x, y = obj[1]
                if speed_x != 0:
                    x += speed_x
                if speed_y != 0:
                    y += speed_y
                obj[1] = (x, y)

    def checkIntersection(self, rect, is_player=True):
        obstacles_rect_list = []
        if is_player:
            keys_rect_list = [key.get_rect(topleft=coord) for key, coord in self.keys]
            for index, key_rect in enumerate(keys_rect_list):
                if key_rect.colliderect(rect):
                    self.keys.pop(index)
                    key_x = len(self.inventory) * 32
                    self.inventory.append([key, (key_x, 0)])

            doors_rect_list = [door.get_rect(topleft=coord) for door, coord in self.doors]
            for door_rect in doors_rect_list:
                if door_rect.colliderect(rect):
                    if not self.inventory:
                        return True
                    else:
                        self.doors.pop(0)
                        self.inventory.pop()
                        return True

        obstacles_rect_list = [obstacle.get_rect(topleft=coord) for obstacle, coord in self.obstacles]
        for obs_rect in obstacles_rect_list:
            if obs_rect.colliderect(rect):
                return True
        return False


class Enemy():
    def __init__(self):
        pass

    def addEnemy(self, img, coord):
        enemies.append([img, coord])
        directions_history[len(directions_history)] = [[], 'right', 2, coord]


enemies = []
directions_history = {}
background = pygame.image.load('images/background.png')
screen = pygame.display.set_mode((300, 300))
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
obstacles_rect_list = []
keys_rect_list = []
door_ver = pygame.image.load('images/door_ver.png')
door_hor = pygame.image.load('images/door_hor.png')
doors = [
    [door_ver, (768, 528)]
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


key = pygame.image.load('images/key.png')
keys = [
        [key, (480, 1008)],
        [key, (96, 96)]
    ]
