# state = [(2, 2), (1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
# this list is the (x,y) position of the respective tile.
# the empty tile is the zero position, 


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

nil = []
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

# will return a list of (x,y) values where the zero tile could be moved
def legal_moves(state):
    # grab the zero tile
    zero = state[0]
    x,y = zero # x,y = (2,2) for example
    # cartesian product of one value and possible moves of the other value
    ymoves = [(x,b) for b in moves[y]]
    xmoves = [(a,y) for a in moves[x]]
    return ymoves + xmoves

## apply_move(create_board("123405678"),(1,2)) == create_board("123045678")
#. True
def apply_move(state,move):
    tileindex  = tile_at(state,move) # where's the tile to swap with zero?
    state = list(state) # argh
    zero = state[0] # get zero
    tile = state[tileindex] # get the other tile
    state[0] = tile # put the other tile (x,y) into the zero tile location
    state[tileindex] = zero # put the previous zero tile location into the other tile location
    return tuple(state)

## len(succ_states(create_board("123405678"))) == 4
#. True
def succ_states(state):
    # which tiles could zero tile move to from here?
    return [apply_move(state,m) for m in legal_moves(state)]

def goal_found(g,node):
    print "goal has been found"
    print "steps are:"
    steps = []
    while(node[3]):
        steps.append(node[2])
        node = node[3]
    steps.append(node[2]) # start state
    steps.reverse()
    for s in steps:
        print show_board(s)
    print show_board(g)
    print

start_board = create_board("617285340")
goal_board = create_board("187206345")

## state_dist(start_board,goal_board) == 6
#. True

# priority will always be (moves_from_start + heuristic_to_goal)
# second value is moves from start, for easy incrementing
# third value is the board_state
# fourth value is the parent board_state, None for the start_board
# this returns the open set as a priority queue
def init_state(start_board,goal_board):
    return [(state_dist(start_board,goal_board),0,start_board,None)]
# closed set, dictionary for easy lookup
closed = {}
# open set is the priority queue from init_state
def solve_step(pqueue,closed,goal_board):
    if(not pqueue):
        # no more states to explore, no solution found
        # do something useful here!
        pass
    pqueue.sort() # sort in order of moves_from_start + heuristic_to_goal
    parent_node = pqueue.pop() # get the least cost node
    # unpack the four tuple, ignore the sort value
    p,parent_moves,parent_board_state,parent = parent_node

    closed[parent_board_state] = parent_moves

    # find the successor board states
    # if they're in the closed set, don't add them XXX should this check closed set cost and update?
    # otherwise, calculate their heuristic cost, add that to the parent move value + 1 and return the new state
    succs = succ_states(parent_board_state)
    for s in succs:
        this_moves = parent_moves + 1
        this_dist  = state_dist(s,goal_board)
        if (this_dist == 0):
            # goal FOUND, we are DONE!
            goal_found(s,parent_node)
            return '' # umm, termination condition?
        if s in closed:
            if(closed[s] > this_moves): # aha! a shorter path to this node! UPDATE THE PQUEUE!
                pqueue.append(this_moves + this_dist,this_moves,s,parent_node)
            continue # We've already got one, NEXT!
        pqueue.append((this_moves + this_dist,this_moves,s,parent_node))
    return (pqueue,closed)

def main():
    goal_board = create_board("123405678")
    start_board = create_board("123450678")
    init = init_state(start_board,goal_board)
    closed = {}
    while (solve_step(init,closed,goal_board)):
        print 'next step!'

if __name__ == '__main__':
    main()

# board state also keeps g (cost so far)
# possibly h, possibly g, possibly f
# possibly a pointer to the previous node

# priority queue of nodes so you can pick the cheapest step each time

# init by putting start node on the priority queue
# check to see if there's anything on the list
# pull from priority queue, are you goal? done
# if nothing on queue, fail
# otherwise call next/succ for moves that slide the zero tile

# generate succ states by checking zero tile position
# if sub 1 from x or y and is less than min, cannot move there
# if add 1 to x or y and is more than max, cannot move there

# jerkins created an enum type to find legal moves
# enum moves { left=1,right=2,up=4,down=8 }
# still had to calculate legal moves, but returned a mask value to say what moves are legal

# output to console is the sequence of states leading to the goal
# give up if you don't find it after 1000 moves or so
