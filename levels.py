# levels.py
LEVEL_CONFIGS = {
    1: {
        'enemies': [
           {'img': 'images/ghost/ghost_right.png', 'pos': (288, 1008)},
        ],
        'keys': [
            {'img': 'images/key.png', 'pos': (80, 528)},
            {'img': 'images/key.png', 'pos': (480, 1008)},
            {'img': 'images/key.png', 'pos': (432, 1200)}
        ],
        'doors': [
            {'img': 'images/door_hor.png', 'pos': (160, 480)},
            {'img': 'images/door_hor.png', 'pos': (800, 1248)},
            {'img': 'images/door_ver.png', 'pos': (320, 144)}
        ]
    },
    2: {
        'enemies': [
            {'img': 'images/ghost/ghost_right.png', 'pos': (256, 1200)},
            {'img': 'images/ghost/ghost_right.png', 'pos': (288, 1008)}
        ],
        'keys': [
            {'img': 'images/key.png', 'pos': (256, 816)},
            {'img': 'images/key.png', 'pos': (336, 816)},
            {'img': 'images/key.png', 'pos': (32, 912)},
            {'img': 'images/key.png', 'pos': (128, 1200)},
            {'img': 'images/key.png', 'pos': (480, 336)}
        ],
        'doors': [
            {'img': 'images/door_hor.png', 'pos': (800, 1248)},
            {'img': 'images/door_ver.png', 'pos': (640, 528)},
            {'img': 'images/door_ver.png', 'pos': (192, 816)},
            {'img': 'images/door_hor.png', 'pos': (96, 384)}
        ]
    },
    3: {
        'enemies': [
            {'img': 'images/ghost/ghost_right.png', 'pos': (32, 48)},
            {'img': 'images/ghost/ghost_right.png', 'pos': (352, 48)},
            {'img': 'images/ghost/ghost_righte.png', 'pos': (160, 720)},
            {'img': 'images/ghost/ghost_right.png', 'pos': (288, 1200)},
        ],
        'keys': [
            {'img': 'images/key.png', 'pos': (672, 48)},
            {'img': 'images/key.png', 'pos': (256, 816)},
            {'img': 'images/key.png', 'pos': (400, 912)},
            {'img': 'images/key.png', 'pos': (272, 1008)},
            {'img': 'images/key.png', 'pos': (416, 1024)},
        ],
        'doors': [
            {'img': 'images/door_ver.png', 'pos': (320, 144)},
            {'img': 'images/door_ver.png', 'pos': (784, 720)},
            {'img': 'images/door_ver.png', 'pos': (208, 912)},
            {'img': 'images/door_ver.png', 'pos': (784, 1104)},
        ]
    }
}