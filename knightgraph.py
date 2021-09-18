'''
State: position, number, previous node(s), after node
Region: Position, number
Ways to invalidate a move: Out of board, does not match given state,sum not matching any other region

Similar to knight's tour, except there's a point where the regions have the same sum with fixed points available

Given a region and order configuration, return the solved puzzle grid

Strategy: use depth-first search to pursue one whole path we meet a breaking condition
* Memoization will not help since the moves keep incrementing and each game board is different 

1. Construct graph, which is pruned by valid moves, given points
2. Search tree for region equivalence until all fixed points are gone through
- How much imbalance needs to exist before we cutoff the search?
3. Return the end grid state for the first path where there's region equivalency


Pick the previous moves that will get you numbers in the smallest regions bidirectionally
- region with lowest number of moves
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
    def __init__(self, grid, regions, move_limit=0, grid_data={}, region_data=[]):
        self.grid = grid
        self.dim = len(self.grid)
        self.move_limit = move_limit

        if move_limit == 0: 
            self.move_limit = self.dim**2

        self.regions = regions
        self.grid_data = grid_data
        self.region_data = region_data

        if len(region_data) == 0:
            self.process_inputs()

    def process_inputs(self):
        num_regions = max([max(x) for x in self.regions])+1
        for x in range(0,num_regions):
            self.region_data.append({
                "sum": 0,
                "zeros": 0,
                "count": 0
            })

        for x in range(0, self.dim):
            for y in range(0, self.dim):
                if self.grid[x][y] != 0:
                    self.grid_data[self.grid[x][y]] = [x,y]
                    self.region_data[self.regions[x][y]]["sum"] += self.grid[x][y]
                else:
                    self.region_data[self.regions[x][y]]["zeros"] += 1
                self.region_data[self.regions[x][y]]["count"] += 1
        
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
        Valid moves check, to reduce the 8^dim**2 possible move parameters 
        - in the board
        - connected to the next move if present
        - is a knight move
        - does not lead to a region having a higher sum than the greatest potential sum of any other region
        - is not greater than the move limit
    '''
    def is_valid_move(self, c, previous_move_num, d):
        
        # pdb.set_trace()
        # print(f"Testing move {previous_move_num+d} at {c}")

        if c[0] >= self.dim or c[1] >= self.dim or c[0] < 0 or c[1] < 0:
            # print(f"    Not in board")
            return False

        if self.grid[c[0]][c[1]] not in [0, previous_move_num+d]:
            # print(f"    Already occupied")
            return False

        if previous_move_num+2*d in self.grid_data:
            n_pos = self.grid_data[previous_move_num+2*d]
            dist = (n_pos[0]-c[0])**2+(n_pos[1]-c[1])**2            
            if dist != 5:
                # print(f"    Does not create continuity with next move")
                return False
        
        if self.grid[c[0]][c[1]] != previous_move_num+d:
            candidate_region_data = deepcopy(self.region_data)
            candidate_region_data[self.regions[c[0]][c[1]]]["sum"] += previous_move_num+d
            candidate_region_data[self.regions[c[0]][c[1]]]["zeros"] -= 1
            
            # minimum total potential sum across the regions. No region's current sum should exceed this value
            # If region A has sum X and region B has sum Y, X > Y but B has no more slots, 
            # then its impossible for this board to work out
            max_achievable_sum = min([x["sum"]+(self.move_limit)*x["zeros"] for x in candidate_region_data])
            max_sum = max(x["sum"] for x in candidate_region_data)
            num_regions = len(candidate_region_data)
            
            # test whether board is relatively unbalanced or absolutely unbalanced
            # board total region sum is equal to moves*(moves+1)/2. 
            # No one region can exceed total region sum / num_regions
            
            max_target_sum = self.move_limit*(self.move_limit+1) / 2.0 / num_regions

            if max_sum > min([max_target_sum, max_achievable_sum]):
                # print(f"     Regions can never be equal with this move Max Achievable: {max_achievable_sum}, Max Sum: {max_sum}, Max Target: {max_target_sum}")
                # print(np.matrix(self.grid))
                return False
            #divisibility constraints
            # if maximum achievable sum is less than the target based on the move limit, then we want to abort
            # print(self.move_limit)
            # print(self.dim**2)
            if self.move_limit != self.dim**2:
                if max_achievable_sum < max_target_sum:
                    # print(f"     Regions can never be equal with this move Max Achievable: {max_achievable_sum}, Max Sum: {max_sum}, Max Target: {max_target_sum}")
                    return False

        return True


    def generate_valid_moves(self, previous_move_num, d): 
        moves = []
        for x in range(0, len(knight_moves)):
            moves.append(False)
        
        # pdb.set_trace()
        if previous_move_num not in self.grid_data or previous_move_num >= self.move_limit:
            return moves
        
        pos = self.grid_data[previous_move_num]
        
        for idx,dm in enumerate(knight_moves):
            c = [pos[0]+dm[0], pos[1]+dm[1]]
            
            if self.is_valid_move(c, previous_move_num, d):
                new_grid_data = copy(self.grid_data)
                new_grid_data[previous_move_num+d] = c

                new_grid = deepcopy(self.grid)
                new_grid[c[0]][c[1]] = previous_move_num+d
                
                new_region_data = deepcopy(self.region_data)
                new_region_data[self.regions[c[0]][c[1]]]["sum"] += previous_move_num+d
                new_region_data[self.regions[c[0]][c[1]]]["zeros"] -= 1


                moves[idx] = Node(new_grid, self.regions, self.move_limit, new_grid_data, new_region_data)
                # pdb.set_trace()
            else:
                moves[idx] = False
        return moves
    
    def answer(self):
        return sum([max(x)**2 for x in self.grid])
    
def search_graph(current_node, level=0):
    # print(f"Level {level}")
    # print("___")
    # print(np.matrix(current_node.grid))
    # print(np.matrix(current_node.region_data))
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
