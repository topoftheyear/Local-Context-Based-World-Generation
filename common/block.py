import pygame
import random

from config import *
from common.enums import BlockType
from common.helpers import random_bool


class Block(pygame.sprite.Sprite):
    def __init__(self, im, x=0, y=0, true_y=0):
        super().__init__()

        self.x = x
        self.y = y
        self.true_y = true_y
        self.type = None

        self.falling = False
        self.settling = False

        self.internal_timer = 0
        self.update_timer = 1
        
        self.image = pygame.image.load(im).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def update(self, block_map):
        self.internal_timer += 1
        self.y += BLOCK_SPEED
        self.rect = self.rect.move(self.x, self.y)
        self.rect.topleft = [self.x, self.y]

        if self.internal_timer >= self.update_timer:
            self.internal_timer = 0
            self.block_life_update(block_map)

    def move_inside_map(self, x, y, block_map):
        # Change blocks position in the block map
        block_map[(self.x, self.true_y)] = None

        self.x += x
        self.y += y
        self.true_y += y

        block_map[(self.x, self.true_y)] = self

        self.rect = self.rect.move(self.x, self.y)
        self.rect.topleft = [self.x, self.y]

    def replace_image(self, im):
        self.image = pygame.image.load(im).convert()

    def physics_update(self, block_map):
        if self.falling:
            self.fall(block_map)
        if self.settling:
            self.settle(block_map)

    def block_life_update(self, block_map):
        pass

    def fall(self, block_map):
        p = (self.x, self.true_y + 8)
        if p in block_map and block_map[p] is None:
            self.move_inside_map(0, 8, block_map)
        else:
            self.falling = False

    def settle(self, block_map):
        # Check below for open space
        self.falling = True
        self.fall(block_map)

        # If it has not fallen, check neighbors for open space
        if self.falling is False:
            pl = (self.x - 8, self.true_y)
            pr = (self.x + 8, self.true_y)
            options = list()
            if pl in block_map and block_map[pl] is None:
                options.append(pl)
            if pr in block_map and block_map[pr] is None:
                options.append(pr)

            # If there is a spot to move to, pick one randomly
            if len(options) > 0:
                p = random.choice(options)
                self.move_inside_map(p[0] - self.x, 0, block_map)
            else:
                self.settling = False


def create_block(block_type, x=0, y=0, true_y=0):
    block = None
    if block_type == BlockType.stone:
        block = Stone(x, y, true_y)
    elif block_type == BlockType.dirt:
        block = Dirt(x, y, true_y)
    elif block_type == BlockType.water:
        block = Water(x, y, true_y)
    elif block_type == BlockType.sand:
        block = Sand(x, y, true_y)

    return block


class Stone(Block):
    def __init__(self, x=0, y=0, true_y=0):
        super().__init__('images/stone.png', x, y, true_y)
        self.type = BlockType.stone
        self.update_timer = float('INF')

    def block_life_update(self, block_map):
        # Stone does nothing
        pass


class Dirt(Block):
    def __init__(self, x=0, y=0, true_y=0):
        super().__init__('images/dirt.png', x, y, true_y)
        self.type = BlockType.dirt
        self.update_timer = random.randint(1, 6) * FPS

    def block_life_update(self, block_map):
        # Dirt may fall
        if random_bool(40):
            self.falling = True

        # Dirt may grow grass if nothing above it
        p = (self.x, self.true_y - 8)
        if random_bool(2):
            if p in block_map and block_map[p] is None:
                self.replace_image('images/grass.png')
        # Grass dies if something is above it
        if p in block_map and block_map[p] is not None:
            self.replace_image('images/dirt.png')


class Water(Block):
    def __init__(self, x=0, y=0, true_y=0):
        super().__init__('images/water.png', x, y, true_y)
        self.type = BlockType.water
        self.update_timer = 1

    def block_life_update(self, block_map):
        # Water settles
        self.settling = True


class Sand(Block):
    def __init__(self, x=0, y=0, true_y=0):
        super().__init__('images/sand.png', x, y, true_y)
        self.type = BlockType.sand
        self.update_timer = 1

    def block_life_update(self, block_map):
        # Sand falls
        self.falling = True
