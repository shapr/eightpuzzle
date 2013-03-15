
# pair = (x,y)

goal = [(2,2),(1,1),(2,1),(3,1),(3,2),(3,3),(2,3),(1,3),(1,2)]

oneaway = goal = [(2,2),(1,1),(2,1),(3,1),(3,2),(3,3),(2,3),(1,3),(1,2)]

def showstate(state):
    line = "-------"
    top = "|%s|%s|%s|" % tuple([tileat(state,pos) for pos in [(1,1),(2,1),(3,1)]])
    mid = "|%s|%s|%s|" % tuple([tileat(state,pos) for pos in [(1,2),(2,2),(3,2)]])
    bot = "|%s|%s|%s|" % tuple([tileat(state,pos) for pos in [(1,3),(2,3),(3,3)]])
    return '\n'.join([line,top,line,mid,line,bot,line])

def tileat(state,(x,y)):
    return state.index((x,y))

nil = []

def dist(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def statedist(sa,sb):
    [dist(a,b) for (a,b) in zip(sa,sb)]
