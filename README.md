# Local-Context-Based-World-Generation
A test project using Pygame to see the viability of using nearby blocks
to inform what the current block should be. This allows for highly 
customizable in-place block spawning for live world generation, so an 
entire world doesn't need to be generated first. Basic water settling
exists here as well as dirt occasionally falling and growing grass.

![](https://user-images.githubusercontent.com/14948706/71793332-18a8b980-3002-11ea-9380-c6237e9e86c9.png)

## How it Works
### Context
Every block type is given a dictionary with references to other block
types and a value. This is called the block's context. As an example,
dirt blocks have the following context:
```python
context = {
    BlockType.dirt: 79,
    BlockType.none: 10,
    BlockType.stone: 10,
    BlockType.water: 1,
}
```
When attempting to spawn a new block and a neighbor is dirt, this is
the context that is received. The dictionary is simple, each block type
has a value associated with it that is its weight. These numbers total
to 100 for convenience but they don't have to. Given the neighbor is
dirt, then the current block has a weighted random chance of being any
of the types listed in its context. So, it has a 79% chance of being
dirt, 10% nothing (open air / cave), 10% stone, and 1% water. Given the
odds, the newly spawned block will likely be dirt.

### Picking the Neighbors
There are many different ways to select nearby context and each provides
different results. As there was no immediately correct way to gather
local context, a variety of ways are picked at random to create variety
in the appearance. As an example though, assume we take the block above 
and blocks around it as context:
```
[STONE    ][STONE   X][DIRT     ]
[DIRT    X][    ?    ][STONE   X]
```
We would get the contexts of each of these marked blocks and sum them 
together. Dirt was already listed above, but assume for this context of
stone:
```python
context = {
    BlockType.stone: 95,
    BlockType.dirt: 5,
}
```
Dirt taken once, stone taken twice would lead to a final summary context
of this:
```python
context = {
    BlockType.dirt: 89,
    BlockType.none: 10,
    BlockType.stone: 200,
    BlockType.water: 1,
}
```

Those values then used as weights and converted to a percentage over the
total number show finally:
```
Dirt: 29.6%
None: 3.3%
Stone: 66.6%
Water: 0.3%
```
Likelihood shows the block to be placed should be stone, though dirt
also has good odds. Going with stone, the end placement should like the
following.
```
[STONE    ][STONE    ][DIRT     ]
[DIRT     ][STONE    ][STONE    ]
```

## Customization
![](https://user-images.githubusercontent.com/14948706/71793165-3e818e80-3001-11ea-9f9e-123ca58729af.png)
An example of a world where blocks have a weight of 99 to themselves,
no water. Only the 'horizontal' context blocks used.

Context can be changed to point any blocks towards each other with any
weights. Multiple styles of blocks used for context can also be modified
or appended to. Here are a few examples.

![](https://user-images.githubusercontent.com/14948706/71793146-2a3d9180-3001-11ea-881e-ceff95984752.png)
Weights unchanged, 'left' and 'right' context blocks used.

![](https://user-images.githubusercontent.com/14948706/71793171-48a38d00-3001-11ea-915e-bd7b846a6cc8.png)
None weight to itself reduced by 4 to 95, 'top' context blocks used.

![](https://user-images.githubusercontent.com/14948706/71793181-52c58b80-3001-11ea-845c-0057a663182a.png)
All blocks point to every other block with a weight of 1.
