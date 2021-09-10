'''
State: position, number, previous node(s), after node
Region: Position, number
Ways to invalidate a move: Out of board, does not match given state,sum not matching any other region
'''
'''
Given a region and order configuration, return the solved puzzle grid

Strategy: use depth-first search to pursue one whole path we meet a breaking condition
* Plus memoization to keep game states

1. Construct graph, which is pruned by valid moves, given points
2. Search tree for region equivalence until all fixed points are gone through
- How much imbalance needs to exist before we cutoff the search?
3. Return the end grid state for the first path where there's region equivalency

'''
import numpy as np
from copy import copy, deepcopy
import pdb

knight_moves = []
steps = [[-1,1], [[1,2],[2,1]]]
for a in steps[0]:
    for b in steps[0]:
        for c in steps[1]:
            knight_moves.append([a*c[0], b*c[1]])        
# print(knight_moves)

class Node():
    data = {}
    regions = []
    region_sums = []
    grid = []
    dim = 0

    def __init__(self, grid, regions):
        self.grid = deepcopy(grid)
        self.dim = len(self.grid) 
        self.data = {}
        self.regions = regions
        self.region_sums = []
        
        num_regions = max([max(x) in regions])
        for x in range(0, num_regions):
            self.region_sums.append(0)
            self.complete_regions.append(0)

        for x in range(0, self.dim):
            for y in range(0, self.dim):
                if self.grid[x][y] != 0:
                    self.data[self.grid[x][y]] = [x,y]
                    self.region_sums[self.regions[x][y]] += grid[x][y]

        

    
    def __init__(self, grid_data, regions, region_sums, complete_regions):
        self.data = {}
        self.data = deepcopy(grid_data)

        self.regions = regions
        self.region_sums = region_sums
        self.complete_regions = complete_regions

    def regions_equivalent(self):
        if len(list(set(self.region_sums))) == 1:
            return True        
        return False
    
    def min_step(self):
        return min([min(x) for x in self.grid])

    def next_empty_move(self):
        for x in range(2, self.dim**2+1):
            if x not in self.data:
                return x-1

        return False

    '''
        Valid moves
        - in the board
        - connected to the next move if present
        - is a knight move
        - does not lead to a region having a higher sum than a complete region
    '''
    def is_valid_move(self, c, previous_move_num, d):
        if c[0] >= self.dim or c[1] >= self.dim or c[0] < 0 or c[1] < 0:
            return False
        
        if previous_move_num+d in self.data:
            if self.data[previous_move_num+d] != c:
                return False

        if previous_move_num+2*d in self.data:
            n_pos = self.data[previous_move_num+2*d]
            dist = (n_pos[0]-c[0])**2+(n_pos[1]-c[1])**2
            # print(f"Current move {previous_move_num}, distance to existing move {dist}")
            
            if dist != 5:
                return False
        
        return True


    def generate_valid_moves(self, previous_move_num, d): 
        # d so we can generate moves from 2 -> 1
        # knight_moves = []
        # steps = [[-1,1], [[1,2],[2,1]]]
        # for a in steps[0]:
        #     for b in steps[0]:
        #         for c in steps[1]:
        #             knight_moves.append([a*c[0], b*c[1]])

        moves = []
        for x in range(0, len(knight_moves)):
            moves.append(False)
        

        if previous_move_num not in self.data:
            return moves
        
        pos = self.data[previous_move_num]
        
        

        for idx,dm in enumerate(knight_moves):
            c = [pos[0]+dm[0], pos[1]+dm[1]]
            
            if self.is_valid_move(c, previous_move_num, d):
                new_data = deepcopy(self.data)
                new_data[previous_move_num+d] = c
                
                new_region_sums = deepcopy(self.region_sums)
                new_region_sums[regions[c[0]][c[1]]] += previous_move_num+d

                new_region_complete =  deepcopy(self.region_complete)
                

                moves[idx] = Node(new_data)
                # pdb.set_trace()
            else:
                moves[idx] = False
        return moves
    
    def answer(self):
        return sum([max(x)**2 for x in self.grid])
    
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


# test_root = Node(completed_grid)
# print(test_root.regions_equivalent(regions))


    
def search_graph(regions, current_node):
    
    if current_node.regions_equivalent(regions):
        print(np.matrix(current_node.grid))
        print(current_node.answer())
        return True
    
    previous_move_num = current_node.next_empty_move()
    moves = current_node.generate_valid_moves(previous_move_num, 1)
    
    for move in moves:
        if move != False:
            # print("---")
            # print(np.matrix(current_node.grid))

            # print(f"Attempting to move from {previous_move_num}({move.data[previous_move_num]}) to {previous_move_num+1}({move.data[previous_move_num+1]})")
            # print(np.matrix(move.grid))
            # print("---")
            search_graph(regions, move)
    pass


# Solution for large regions

# root = Node(practice_grid)
# search_graph(root)

root = Node(large_grid)
moves = root.generate_valid_moves(2, -1)
for move_root in moves:
    if move_root != False:
        print(" ")
        print(np.matrix(move_root.grid))
        search_graph(large_regions, move_root)
# print(root.next_empty_move())
# root.generate_valid_moves(1,1)

