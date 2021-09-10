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
class Node():
    pos = [0,0]
    num = 0
    children = {}

    def __init__(self, pos, num):
        self.pos = pos
        self.num = num
    
    def set_child(self, idx, new_node):
        self.children[idx] = new_node

'''
    This is the main class that constructs the graph of possibilities for the knights taking into consideration:
    1. Fixed points given in the problem
    2. Valid moves based on board size and sequential knight movement

    And conducts DFS on the graph until a path is discovered where regions have equivalent sums
'''

class KnightGraph():
    root = Node()
    regions = []
    num_regions = []
    dim = 0
    grid = []
    data = {}
    dm = []
    move_order = {}
    self.num_moves = 0

    def __init__(self, regions, grid):
        self.root = Node()
        self.regions = regions
        self.grid = grid
        self.num_regions = max([max(y) for y in regions])+1
        self.dim = len(self.grid)

        for x in range(0, self.dim):
            for y in range(0, self.dim):
                if self.grid[x][y] != 0:
                    self.data[grid[x][y]] = [x,y]
        
        self.num_moves = max(self.data.keys())+5

        for v in [1,-1]: #up or down
            for w in [1,-1]: # left or right
                for z in [[1,2],[2,1]]: # [1,2] or [2,1]
                    self.dm.append(v*z[0], w*z[1])
        
        # self.dm.sort(key=lambda x: x[0]/4.1+x[1])
        # for move, idx in enumerate(self.dm):
        #     self.move_order[] 
    
    '''
    If each region has the same sum, then true, otherwise false

    '''
    def regions_equivalent(self):
        sums = [0]*self.num_regions
        for x in range(0, self.dim):
            for y in range(0, self.dim):                
                sums[self.regions[x][y]] += self.grid[x][y]

        for x in range(0,len(sums)-1):
            if sums[x] != sums[x+1]:
                return False
        return True

    def get_valid_moves(self,ind):
        moves = {}
        pos1 = [self.data[ind][0], self.data[ind][1]]
        pos2 = []

        if ind+1 in self.data:
            return self.data[ind+1]
        elif ind+2 in self.data:
            pos2 = self.data[ind+2]

        for m,idx in enumerate(dm):
            new_move = [pos1[0]+m[0], pos1[1]+m[1]]
            if new_move[0] >= 0 and new_move[1] >= 0 and new_move[0] < self.dim and new_move[1] < self.dim:
                moves[idx] = new_move
            else:
                moves[idx] = False
        
        return moves
    
    '''
        Hidden node to account for not starting at 1
        If a node has no valid successors, that node is removed from the parent node
        Go point to point forward to find the paths that take x-y+1 steps from step x to step y, x and y are nearest given steps
    '''

    def construct_graph(self):
        # start at 1, if a point is not available keep expanding number of moves
        # if a move and a fixed point do not agree, remove that node
        self.root = Node(self.data[1], 1)
        for x in range(2,self.num_moves):
            if x in self.data:
                


        pass

    '''
        DFS through graph until N steps have passed or region equivalence is found
    '''

    def search_graph(self):
        pass


def is_intermediate_move(candidate, pos2, n):
    if len(pos2) == 0:
        return True

    moves = get_valid_moves(candidate, [], n)
    if pos2 in moves:
        return True
    return False

def find_solved_puzzle(regions, grid):    
    if regions_equivalent(regions, state):
        return grid
    

    data = grid2data(grid)
    n = data["size"]
    # Start with 1, if it doesn't exist populate all zeroes
    if 1 not in data:
        for x in range(0,n):
            for y in range(0,n):
                if grid[x][y] == 0:
                    grid[x][y] = 1
                    test_grid = find_solved_puzzle(regions, grid)
                    if test_grid != False:
                        return test_grid
    
    for x in range(1,n**2-1):
        next_pos = []
        moves = get_valid_moves(data[x], next_pos, n)
        if x not in data:
            for move in valid_moves:
                grid[move[0]][move[1]] = x
                test_grid = find_solved_puzzle(regions, grid)
                if test_grid != False:
                    return test_grid
    
    print("Check for unsolvability")
    return False
        



    
    

    

    pass

