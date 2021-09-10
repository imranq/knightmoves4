from knightgraph import *
import unittest

region1 = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,1,0,0,0],
    [1,1,1,1,0],
    [1,2,2,0,0],
]

grid = [
    [1,0,3,0,0],
    [0,0,0,0,4],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,6,0,0,0],
]

order1_complete = [
    [1,0,3,0,0],
    [0,0,0,0,4],
    [0,2,7,0,0],
    [8,0,0,5,0],
    [0,6,9,0,0],
]


data = grid2data(grid)
print(data)
moves = get_valid_moves(data, 1)
for move in moves:
    print(move)




