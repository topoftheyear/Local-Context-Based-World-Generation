import os
import random

import numpy as np
import pygame
from pygame.locals import *

from common.enums import BlockType
from config import *
from common.helpers import *

from common.block import *
from common.block_contexts import *


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Gen Test')

        self.font = pygame.font.Font(None, 30)
        self.clock = pygame.time.Clock()

        self.block_map = dict()
        self.blocks = pygame.sprite.Group()

        self.y = -8
        self.block_spawn_offset = 0

        self.current_context_points = None
        
        self.loop()
        
    def loop(self):
        while True:
            self.screen.fill((0, 0, 0))

            if self.y + self.block_spawn_offset <= SCREEN_HEIGHT + 32:
                self.generate()

            self.update()
            self.check_input()
            self.draw_screen()
            pygame.display.flip()
            self.clock.tick(FPS)
            
    def check_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit(0)
                
    def draw_screen(self):
        for block in self.blocks.sprites():
            if -8 <= block.x <= SCREEN_WIDTH and -8 <= block.y <= SCREEN_HEIGHT:
                self.screen.blit(block.image, block.rect)

        fps = self.font.render(str(int(self.clock.get_fps())), True, pygame.Color('white'))
        self.screen.blit(fps, (50, 50))

    def update(self):
        self.block_spawn_offset += BLOCK_SPEED

        keys_to_delete = list()
        for key, block in self.block_map.items():
            if block is not None:
                # Update block
                block.update(self.block_map)

            # Kill blocks
            if key[1] + self.block_spawn_offset < -8:
                self.blocks.remove(block)
                del block
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self.block_map[key]

        # Physics updates on the blocks
        for key, block in self.block_map.items():
            if block is not None:
                block.physics_update(self.block_map)

    def generate(self):
        self.y += 8

        # Deal with current points
        if self.current_context_points is None or random_bool(CONTEXT_CHANGE_FREQUENCY_DENOMINATOR):
            total_weight = sum([_ for _ in CONTEXT_WEIGHTS.values()])
            weights = [k / total_weight for k in CONTEXT_WEIGHTS.values()]
            new_point = np.random.choice([_ for _ in CONTEXT_POINTS.keys()], p=weights)
            self.current_context_points = new_point

        proposed_row = list()
        iterator = None

        # Determine proper direction
        if self.current_context_points is 'left':
            iterator = range(0, SCREEN_WIDTH, 8)
        elif self.current_context_points is 'right':
            iterator = range(SCREEN_WIDTH + 8, -1, -8)
        else:
            iterator = random.choice([range(0, SCREEN_WIDTH, 8), range(SCREEN_WIDTH + 8, -1, -8)])

        proposed_row = self.generate_line(iterator, CONTEXT_POINTS[self.current_context_points])

        # Create the proposed row
        for info in proposed_row:
            block_type, x = info

            if block_type == BlockType.none:
                self.block_map[(x, self.y)] = None
                continue

            block = create_block(block_type, x=x, y=self.y + self.block_spawn_offset, true_y=self.y)
            self.block_map[(x, self.y)] = block
            self.blocks.add(block)

    def generate_line(self, iter, context_points=None):
        # Go horizontally through the world to create proposed row of blocks
        proposed_row = list()
        for x in iter:
            if context_points is None:
                context_points = random.choice([_ for _ in CONTEXT_POINTS.values()])

            # Get nearby blocks to generate context
            total_context = dict()
            for offset in context_points:
                p = (x + offset[0], self.y + offset[1])

                # Get block context
                current_context = dict()
                # Check if it exists in the map
                if p in self.block_map:
                    block = self.block_map[p]

                    # Block left intentionally empty
                    if block is None:
                        current_context = get_block_context(block_type=BlockType.none)
                    else:
                        current_context = get_block_context(block)
                # Block not found in the current map, consult the proposed row
                else:
                    for block in proposed_row:
                        if p[0] == block[1]:
                            current_context = get_block_context(block_type=block[0])
                            break

                total_context = merge_sum_dictionaries(total_context, current_context)

            # Check to make sure context exists, if not, set to context for BlockType.stone
            if len(total_context.keys()) == 0:
                total_context = get_block_context(block_type=BlockType.stone)

            # Weighted random pick the block given the context
            new_type = weighted_random_from_dict(total_context)

            # Add block to list
            proposed_row.append([new_type, x])

        return proposed_row


if __name__ == "__main__":
    pygame.init()
    g = Game()
