'''
Following Knight Graph, this version uses an explorer node with no recursion
Node will make moves and undo them to go to the next move
Has a state of current move with a move array
Has a state of choice of knight move
Has a make_next_move and undo functions

Board language
[0,0,0,0]
[1,2,4,5]

Understand
- Is this approach faster than recursion
- Use less memory?

'''
import numpy as np
import pdb
from collections import OrderedDict


class NodeExplorer():
    def __init__(self, grid, regions, move_limit=0):
        self.grid = grid
        self.regions = regions
        self.dim = len(self.grid)
        self.move_limit = move_limit
        self.move_history = [] # only moves that are chosen
        self.move_states = [] # array with move history with knight states from 1 to 8. Given points are given -1
        self.grid_data = []
        self.region_data = []
        self.knight_moves = []
        self.num_regions = max([max(x) for x in self.regions])+1

        if move_limit == 0: 
            self.move_limit = self.dim**2

        
        steps = [[-1,1], [[1,2],[2,1]]]
        for a in steps[0]:
            for b in steps[0]:
                for c in steps[1]:
                    self.knight_moves.append([a*c[0], b*c[1]])        

        
        for x in range(0,num_regions):
            self.region_data.append({
                "sum": 0,
                "zeros": 0,
                "count": 0
            })

        for x in range(0, self.dim):
            for y in range(0, self.dim):
                if self.grid[x][y] != 0:
                    self.move_states[x*self.dim+y] = 0
                    self.grid_data[self.grid[x][y]] = [x,y]
                    self.region_data[self.regions[x][y]]["sum"] += self.grid[x][y]
                else:
                    self.move_states[x*self.dim+y] = 1
                    self.grid_data[self.grid[x][y]] = []
                    self.region_data[self.regions[x][y]]["zeros"] += 1
                self.region_data[self.regions[x][y]]["count"] += 1

    # update grid, 
    def undo_last_move(self):    
        last_move_num = self.move_history[-1]
        last_move_pos = self.grid_data[self.move_history[-1]]
        self.grid[last_move_pos[0]][last_move_pos[1]] = 0
        self.grid_data[last_move_num] = None
        #increment move state, if at 7, move to 0, and push the previous value up
        carryover = True
        x = self.move_history[-1]
        while carryover and x >= 0:
            if self.move_states[x] != -1:
                self.move_states[x] = (self.move_states[x] + 1) % 8
                if self.move_states[x] == 0:
                    carryover = False
            x -= 1
        pass

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
    def is_valid_move(self, move, move_num, direction):
        # pdb.set_trace()
        # print(f"Testing move {previous_move_num+d} at {c}")

        if move[0] >= self.dim or move[1] >= self.dim or move[0] < 0 or move[1] < 0:
            # print(f"    Not in board")
            return False

        if self.grid[move[0]][move[1]] not in [0, move_num]:
            # print(f"    Already occupied")
            return False

        if move_num+direction in self.grid_data:
            n_pos = self.grid_data[move_number_2]
            dist = (n_pos[0]-move[0])**2+(n_pos[1]-move[1])**2            
            if dist != 5:
                # print(f"    Does not create continuity with next move")
                return False
        
        if self.grid[move[0]][move[1]] != move_num:
            region_num = self.regions[move[0]][move[1]]
            self.region_data[region_num]["sum"] += move_num
            self.region_data[region_num]["zeros"] -= 1
            
            # minimum total potential sum across the regions. No region's current sum should exceed this value
            # If region A has sum X and region B has sum Y, X > Y but B has no more slots, 
            # then its impossible for this board to work out
            max_achievable_sum = min([x["sum"]+(self.move_limit)*x["zeros"] for x in self.region_data])
            max_sum = max(x["sum"] for x in self.region_data)
            
            # test whether board is relatively unbalanced or absolutely unbalanced
            # board total region sum is equal to moves*(moves+1)/2. 
            # No one region can exceed total region sum / num_regions
            
            max_target_sum = self.move_limit*(self.move_limit+1) / 2.0 / self.num_regions
            # if maximum achievable sum is less than the target based on the move limit, then we want to abort

            if (max_sum > min([max_target_sum, max_achievable_sum])) or (self.move_limit != self.dim**2 and max_achievable_sum < max_target_sum):
                # print(f"     Regions can never be equal with this move Max Achievable: {max_achievable_sum}, Max Sum: {max_sum}, Max Target: {max_target_sum}")
                # print(np.matrix(self.grid))
                self.region_data[region_num]["sum"] -= move_num
                self.region_data[region_num]["zeros"] += 1

                return False
                    

        return True


    def make_next_move(self): 
        d = 1
        self.latest_move_num = max(self.grid_data.keys())
        if  not in self.grid_data or latest_move_num >= self.move_limit:
            return False
        
        pos = self.grid_data[latest_move_num]
        km = self.knight_moves[self.move_states[latest_move_num]]

        move = [pos[0]+km[0], pos[1]+km[1]]
        
        if self.is_valid_move(move):
            self.grid_data[latest_move_num+d] = move
            self.grid[move[0]][move[1]] = latest_move_num+d
            self.move_states[latest_move_num]
            return True
        else:
                
    def answer(self):
        return sum([max(x)**2 for x in self.grid])
    
def search_graph(grid, regions):
    explorer = NodeExplorer(grid, regions) 
    
    while explorer.make_next_move():
        if explorer.regions_equivalent():
            print(np.matrix(explorer.grid))
            print(np.matrix(explorer.region_data))
            print(explorer.answer())
            return True            
    pass
