#!/usr/bin/env python
# the line above means if this file is chmod u+x then ./eight.py will work, as long as python is in your $PATH

# Shae Erisson
# CS470-01 2013 assignment #1
# A* solver for the eight puzzle

# board_state = [(2, 2), (1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
# this list is the (x,y) position of the respective tile.
# the state above says the empty tile is the 2,2 position, the 1 tile is in the 1,1 position etc.

# the actual solver function passes around a tuple of four values:
# this_tuple = (h(n)+g(n),g(n),board_state,parent_tuple)
# h(n)+g(n) is first so I can just sort a list instead of using a 'real' priority queue
# g(n) is separate for easy calculating of g(n)+1 for successor board_state tuples
# board_state is the value described above, a list of (x,y) postitions
# parent_tuple is a reference to the predecessor move, for the start state, it will be None

def show_board(board):
    line = "-------"
    top = "|%s|%s|%s|" % tuple([tile_at(board,pos) for pos in [(1,1),(2,1),(3,1)]])
    mid = "|%s|%s|%s|" % tuple([tile_at(board,pos) for pos in [(1,2),(2,2),(3,2)]])
    bot = "|%s|%s|%s|" % tuple([tile_at(board,pos) for pos in [(1,3),(2,3),(3,3)]])
    return '\n'.join([line,top,line,mid,line,bot,line])

## ((2, 2), (1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)) == create_board("123405678")
#. True

def create_board(numbers):
    # must have at least nine numbers in the input string, will act weird if they're not unique
    # 123405678
    positions = [(x,y) for y in [1,2,3] for x in [1,2,3]] # order is important here!
    board = zip(numbers,positions)
    board.sort() # now ordered correctly
    return tuple(map(lambda x:x[1],board)) # strip the values, leave only positions

## 0 == tile_at(create_board("123405678"),(2,2))
#. True

def tile_at(state,(x,y)):
    return state.index((x,y))

## 0 == dist((1,1),(1,1))
#. True
## 1 == dist((1,2),(1,1))
#. True
def dist(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

## 1 == state_dist(create_board("123405678"),create_board("123045678"))
#. True
def state_dist(sa,sb):
    # must leave out the zero for this to work, [1:] drops the first (zero) item
    return sum([dist(a,b) for (a,b) in zip(sa[1:],sb[1:])])

# dictionary of legal moves for both x and y values:
# 1 -> 2; 2 -> 1,3; 3 -> 2
moves = {1:[2],2:[1,3],3:[2]}

# will return a list of (x,y) values of where the zero tile could be moved to
def legal_moves(board_state):
    # grab the zero tile from the state
    zero = board_state[0]
    x,y = zero # x,y = (2,2) for example
    # cartesian product of one value and possible moves of the other value
    ymoves = [(x,b) for b in moves[y]]
    xmoves = [(a,y) for a in moves[x]]
    return ymoves + xmoves

## apply_move(create_board("123405678"),(1,2)) == create_board("123045678")
#. True

# this unattractive function swaps the zero tile with the tile at the position given
def apply_move(board_state,move):
    tileindex  = tile_at(board_state,move) # where's the tile to swap with zero?
    board_state = list(board_state) # cast to a mutable type, argh
    zero = board_state[0] # get zero
    tile = board_state[tileindex] # get the other tile
    board_state[0] = tile # put the other tile (x,y) into the zero tile location
    board_state[tileindex] = zero # put the previous zero tile location into the other tile location
    return tuple(board_state) # cast back to an immutable type for dictionary use, argh

## len(succ_states(create_board("123405678"))) == 4
#. True
def succ_states(state):
    # which tiles could zero tile move to from here?
    return [apply_move(state,m) for m in legal_moves(state)]

def goal_found(g,node,nodes_explored):
    print "goal has been found"
    print "steps are:"
    steps = []
    steps.append(g)
    while(node[3]):
        steps.append(node[2])
        node = node[3]
    steps.append(node[2]) # start state
    steps.reverse()
    for s in steps:
        print show_board(s)
    print "total number of steps taken is ",(len(steps)-1)

# the closed set is a dictionary for easy board_state lookup
closed = {}

# given start and goal board states, return the initial solver state.
def init_state(start_board,goal_board):
    return [(state_dist(start_board,goal_board),0,start_board,None)]

# the four tuple passed around in solver is (h(n)+g(n),g(n),board_state,parent_tuple)
# the four tuple is described further at the top of this file
def solver(pqueue,closed,goal_board):
    nodes_explored = 0
    if(not pqueue):
        # no more states to explore, no solution found
        # do something useful here!
        print "No solution found"
        return 0
    pqueue.sort(reverse=True) # sort in ASCENDING order of moves_from_start + heuristic_to_goal
    parent_node = pqueue.pop() # get the least cost node
    # unpack the four tuple, ignore the sort value
    p, parent_moves, parent_board_state, parent = parent_node
    if parent_moves > 100:
        print "too many steps, giving up"
        return 0 # too many steps
    closed[parent_board_state] = parent_node

    # find the successor board states
    # if they're in the closed set, don't add them
    # this checks closed set cost and reopens nodes with a shorter cost than we had before
    # otherwise, calculate their heuristic cost, add that to the parent move value + 1 and return the new state
    succs = succ_states(parent_board_state)
    for s in succs:
        nodes_explored += 1
        this_moves = parent_moves + 1
        this_dist  = state_dist(s, goal_board)
        if (this_dist == 0):
            # goal FOUND, we are DONE!
            goal_found(s,parent_node,nodes_explored)
            return 0 # umm, termination condition?
        if s in closed:
            if(closed[s][1] > this_moves): # aha! a shorter path to this node! UPDATE THE PQUEUE!
                pqueue.append(this_moves + this_dist,this_moves, s, parent_node)
            continue # We've already got one, NEXT!
        pqueue.append((this_moves + this_dist, this_moves, s, parent_node))
    return (pqueue,closed)

def get_board():
    board_input = raw_input('> ')
    while not (len(board_input) == 9 and board_input.isdigit()):
        print "invalid input, try again."
        board_input = raw_input('> ')
    return board_input

def main():
    print "You can now enter a start and goal board, in the format: 123405678"
    print "start? ex: 287354016"
    start_input = get_board()
    print "goal? ex: 187206345"
    goal_input = get_board()
    goal_board = create_board(goal_input)
    start_board = create_board(start_input)
    if(goal_board == start_board):
        print "start and goal are the same, no work to do"
        return
    init = init_state(start_board,goal_board)
    closed = {}
    while (solver(init,closed,goal_board)):
        #print 'next step!'
        pass

if __name__ == '__main__':
    main()
