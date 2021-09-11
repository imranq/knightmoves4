from knightgraph import *
import time

practice_grid = [
    [1,0,0,0,0],
    [0,0,0,0,4],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,6,0,0,0]
]

completed_practice_grid = [
    [1,0,3,0,0],
    [0,0,0,0,4],
    [0,2,7,0,0],
    [8,0,0,5,0],
    [0,6,9,0,0]
]

practice_regions = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,1,0,0,0],
    [1,1,1,1,0],
    [1,2,2,0,0]
]

large_regions = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,14,0,0,0,0,16,0],
    [0,0,0,14,0,0,0,0,16,0],
    [0,0,14,14,14,14,15,16,16,16],
    [1,0,14,0,0,13,15,15,15,15],
    [1,0,0,0,13,13,13,12,12,15],
    [1,2,2,9,13,10,10,12,12,7],
    [1,3,2,9,9,11,11,11,12,7],
    [1,3,4,9,8,8,8,6,6,7],
    [3,3,4,5,5,5,5,5,6,7],
]

large_grid_data = {
    12: [0,0],
    5: [1,6],
    8: [2,6],
    23: [1,8],
    14: [3,3],
    2: [5,1],
    20: [6,4],
    33: [7,4],
    28: [9,9]
}

large_grid = []
for x in range(0,10):
    large_grid.append([])
    for y in range(0,10):
        large_grid[x].append(0)

for k in large_grid_data.keys():
    large_grid[large_grid_data[k][0]][large_grid_data[k][1]] = k


import time
start_time = time.time()

# root = Node(practice_grid, practice_regions)
# search_graph(root)

root = Node(large_grid, large_regions)
moves = root.generate_valid_moves(2, -1)
for move_root in moves:
    if move_root != False:
        print(" ")
        print(np.matrix(move_root.grid))
        search_graph(move_root)
print("--- %s seconds ---" % (time.time() - start_time))