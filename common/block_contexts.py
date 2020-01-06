from common.enums import BlockType


def get_block_context(block=None, block_type=None):
    if block_type is None:
        if block is None:
            block_type = BlockType.none
        else:
            block_type = block.type

    context = dict()
    if block_type == BlockType.none:
        context = {
            BlockType.none: 99,
            BlockType.dirt: 1,
        }
    elif block_type == BlockType.stone:
        context = {
            BlockType.stone: 95,
            BlockType.dirt: 5,
        }
    elif block_type == BlockType.dirt:
        context = {
            BlockType.dirt: 79,
            BlockType.none: 10,
            BlockType.stone: 10,
            BlockType.water: 1,
        }
    elif block_type == BlockType.water:
        context = {
            BlockType.water: 80,
            BlockType.dirt: 20,
        }
    elif block_type == BlockType.sand:
        context = {
            BlockType.sand: 50,
            BlockType.water: 25,
            BlockType.dirt: 25,
        }

    return context
