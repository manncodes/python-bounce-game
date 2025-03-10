from constants import *

# Define level layouts as a list of lists
# Each number represents a block with a specific color and strength
# 0: No block
# 1-7: Different colored blocks with increasing strength and points

levels = [
    # Level 1 - Simple pattern
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    
    # Level 2 - Pyramid
    [
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 2, 2, 2, 2, 2, 2, 0],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [4, 4, 4, 0, 0, 4, 4, 4],
        [5, 5, 0, 0, 0, 0, 5, 5]
    ],
    
    # Level 3 - Alternating pattern with stronger blocks
    [
        [2, 1, 2, 1, 2, 1, 2, 1],
        [3, 0, 3, 0, 3, 0, 3, 0],
        [4, 4, 4, 4, 4, 4, 4, 4],
        [0, 5, 0, 5, 0, 5, 0, 5],
        [6, 6, 6, 6, 6, 6, 6, 6]
    ],
    
    # Level 4 - Harder level with more durable blocks
    [
        [7, 7, 7, 7, 7, 7, 7, 7],
        [6, 6, 6, 6, 6, 6, 6, 6],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [4, 4, 4, 4, 4, 4, 4, 4],
        [3, 3, 3, 3, 3, 3, 3, 3]
    ]
]

# Color and point value mapping for blocks
block_properties = {
    1: {"color": RED, "points": SCORE_PER_BLOCK, "strength": 1},
    2: {"color": ORANGE, "points": SCORE_PER_BLOCK * 2, "strength": 1},
    3: {"color": YELLOW, "points": SCORE_PER_BLOCK * 3, "strength": 1},
    4: {"color": GREEN, "points": SCORE_PER_BLOCK * 4, "strength": 2},
    5: {"color": BLUE, "points": SCORE_PER_BLOCK * 5, "strength": 2},
    6: {"color": PURPLE, "points": SCORE_PER_BLOCK * 6, "strength": 3},
    7: {"color": WHITE, "points": SCORE_PER_BLOCK * 7, "strength": 3}
}
