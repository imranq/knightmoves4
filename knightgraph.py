'''
State: position, number, previous node(s), after node
Region: Position, number
Ways to invalidate a move: Out of board, does not match given state,sum not matching any other region
'''
'''
Given a region and order configuration, return the solved puzzle grid

Strategy: use depth-first search to pursue one whole path we meet a breaking condition
* Memoization will not help since the moves keep incrementing and each game board is different 

1. Construct graph, which is pruned by valid moves, given points
2. Search tree for region equivalence until all fixed points are gone through
- How much imbalance needs to exist before we cutoff the search?
3. Return the end grid state for the first path where there's region equivalency


Pick the previous moves that will get you numbers in the smallest regions bidirectionally
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
    grid_data = {}
    regions = []
    region_data = []
    grid = []
    dim = 0
    
    def __init__(self, grid, regions, grid_data={}, region_data=[]):
        self.grid = deepcopy(grid)
        self.dim = len(self.grid) 
        self.regions = regions
        self.grid_data = deepcopy(grid_data)
        self.region_data = deepcopy(region_data)

        if len(region_data) == 0:
            self.process_inputs()

    def process_inputs(self):
        num_regions = max([max(x) for x in self.regions])+1
        for x in range(0,num_regions):
            self.region_data.append({
                "sum": 0,
                "zero_count": 0 
            })

        for x in range(0, self.dim):
            for y in range(0, self.dim):
                if self.grid[x][y] != 0:
                    self.grid_data[self.grid[x][y]] = [x,y]
                    self.region_data[self.regions[x][y]]["sum"] += self.grid[x][y]
                else:
                    self.region_data[self.regions[x][y]]["zero_count"] += 1
        
    def regions_equivalent(self):
        if len(list(set([x["sum"] for x in self.region_data]))) == 1:
            return True        
        return False
    
    def min_step(self):
        return min([min(x) for x in self.grid])

    def next_empty_move(self):
        for x in range(2, self.dim**2+1):
            if x not in self.grid_data:
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
        
        # pdb.set_trace()
        if c[0] >= self.dim or c[1] >= self.dim or c[0] < 0 or c[1] < 0:
            return False

        if self.grid[c[0]][c[1]] not in [0, previous_move_num+d]:
            return False

        if previous_move_num+2*d in self.grid_data:
            n_pos = self.grid_data[previous_move_num+2*d]
            dist = (n_pos[0]-c[0])**2+(n_pos[1]-c[1])**2
            # print(f"Current move {previous_move_num}, distance to existing move {dist}")
            
            if dist != 5:
                return False
        
        
        # get the set of all sums where the zero count is 0
        # this set should only have 1 number, otherwise false
        candidate_region_data = deepcopy(self.region_data)

        if self.grid[c[0]][c[1]] != previous_move_num+d:
            candidate_region_data[self.regions[c[0]][c[1]]]["sum"] += previous_move_num+d
            candidate_region_data[self.regions[c[0]][c[1]]]["zero_count"] -= 1


        min_target = min([x["sum"]+(self.dim**2)*x["zero_count"] for x in candidate_region_data])

        for x in range(0, len(candidate_region_data)):
            if candidate_region_data[x]["sum"] > min_target:
                return False
        
        return True


    def generate_valid_moves(self, previous_move_num, d): 
        moves = []
        for x in range(0, len(knight_moves)):
            moves.append(False)
        

        if previous_move_num not in self.grid_data:
            return moves
        
        pos = self.grid_data[previous_move_num]
        
        

        for idx,dm in enumerate(knight_moves):
            c = [pos[0]+dm[0], pos[1]+dm[1]]
            
            if self.is_valid_move(c, previous_move_num, d):
                new_grid_data = deepcopy(self.grid_data)
                new_grid_data[previous_move_num+d] = c

                new_grid = deepcopy(self.grid)
                new_grid[c[0]][c[1]] = previous_move_num+d
                
                new_region_data = deepcopy(self.region_data)
                new_region_data[self.regions[c[0]][c[1]]]["sum"] += previous_move_num+d
                new_region_data[self.regions[c[0]][c[1]]]["zero_count"] -= 1


                moves[idx] = Node(new_grid, self.regions, new_grid_data, new_region_data)
                # pdb.set_trace()
            else:
                moves[idx] = False
        return moves
    
    def answer(self):
        return sum([max(x)**2 for x in self.grid])
    
def search_graph(current_node, level=0):
    print(f"Level {level}")
    print("___")
    print(np.matrix(current_node.grid))
    print(np.matrix(current_node.region_data))
    if current_node.regions_equivalent():
        print(np.matrix(current_node.grid))
        print(np.matrix(current_node.region_data))

        print(current_node.answer())
        return True
    
    previous_move_num = current_node.next_empty_move()
    moves = current_node.generate_valid_moves(previous_move_num, 1)
    for move in moves:
        if move != False:
            search_graph(move, level+1)
    pass
