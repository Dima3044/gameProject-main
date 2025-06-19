# levels.py
LEVEL_CONFIGS = {
    1: {
        'enemies': [
           # {'img': 'images/zombie.png', 'pos': (352, 816)},
        ],
        'keys': [
            {'img': 'images/key.png', 'pos': (96, 96)}
        ],
        'doors': [
            #{'img': 'images/door_ver.png', 'pos': (768, 528)},
            #{'img': 'images/exit_door.png', 'pos': (800, 1248)},
            #{'img': 'images/door_hor.png', 'pos': (736, 480)},
            #{'img': 'images/door_ver.png', 'pos': (640, 528)},
        ]
    },
    2: {
        'enemies': [
            {'img': 'images/zombie.png', 'pos': (500, 400)},
            {'img': 'images/ghost.png', 'pos': (200, 800)}
        ],
        'keys': [
            {'img': 'images/key.png', 'pos': (300, 300)}
        ],
        'doors': [
            {'img': 'images/door_ver.png', 'pos': (700, 200)},
            {'img': 'images/door_hor.png', 'pos': (100, 600)}
        ]
    },
    3: {
        # ... конфигурация для уровня 3 ...
    }
}