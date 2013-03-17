# state = [(2, 2), (1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
# this list is the (x,y) position of the respective tile.
# the empty tile is the zero position, 


def show_state(state):
    line = "-------"
    top = "|%s|%s|%s|" % tuple([tile_at(state,pos) for pos in [(1,1),(2,1),(3,1)]])
    mid = "|%s|%s|%s|" % tuple([tile_at(state,pos) for pos in [(1,2),(2,2),(3,2)]])
    bot = "|%s|%s|%s|" % tuple([tile_at(state,pos) for pos in [(1,3),(2,3),(3,3)]])
    return '\n'.join([line,top,line,mid,line,bot,line])

## ((2, 2), (1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)) == create_state("123405678")
#. True

def create_state(numbers):
    # must have at least nine numbers in the input string, will act weird if they're not unique
    # 123405678
    positions = [(x,y) for y in [1,2,3] for x in [1,2,3]] # order is important here!
    state = zip(numbers,positions)
    state.sort() # now ordered correctly
    return tuple(map(lambda x:x[1],state)) # strip the values, leave only positions

## 0 == tile_at(create_state("123405678"),(2,2))
#. True
def tile_at(state,(x,y)):
    return state.index((x,y))

## 2 + 3
#. 5

nil = []
## 0 == dist((1,1),(1,1))
#. True
## 1 == dist((1,2),(1,1))
#. True
def dist(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

## 1 == state_dist(create_state("123405678"),create_state("123045678"))
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

def apply_move(state,move):
    tileindex  = tile_at(state,move) # where's the tile to swap with zero?
    zero = state[0] # get zero
    tile = state[tileindex] # get the other tile
    state[0] = tile # put the other tile (x,y) into the zero tile location
    state[tileindex] = zero # put the previous zero tile location into the other tile location
    return state

def succstates(state):
    # which tiles could zero tile move to from here?
    legalmoves(state)
    tile_at((2,1))

# pair = (x,y)
#blank = [(0,0) for n in xrange(1,10)]
# 123
# 405
# 678
start = create_state("123405678")
# or [(2,2),(1,1),(2,1),(3,1),(1,2),(3,2),(1,3),(2,3),(3,3)]

oneaway = [(2,2),(1,1),(2,1),(3,1),(3,2),(3,3),(2,3),(1,3),(1,2)]

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
