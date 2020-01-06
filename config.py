FPS = 120

WORLD_WIDTH = 160
WORLD_HEIGHT = 90

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BLOCK_SPEED = -1

CONTEXT_CHANGE_FREQUENCY_DENOMINATOR = 6
CONTEXT_POINTS = {
    'top': [[-8, -8], [0, -8], [8, -8]],
    'left': [[-8, 0], [0, -8]],
    'right': [[8, 0], [0, -8]],
    'horizontal': [[-8, 0], [0, -8], [8, 0]]
}

CONTEXT_WEIGHTS = {
    'top': 5,
    'left': 25,
    'right': 25,
    'horizontal': 45,
}
