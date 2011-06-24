from heapq import heappush, heappop # for priority queue
import time
import math
import random
from strings import *

class node:
    x = 0 # x pos
    y = 0 # y pos
    dist = 0 # total distance already moved to get to to the finish
    pr = 0 # priority = distance + remaining estimated distance
    
    def __init__(self, x, y, dist, pr):
        self.x = x
        self.y = y
        self.dist = dist
        self.pr = pr
        
    def __lt__(self, other): # comparison method for priority queue
        return self.pr < other.pr
    
    def update_pr(self, x_dest, y_dest):
        self.pr = self.dist + self.estimation(x_dest, y_dest) * 10 # A*
        
    # give higher priority to going straight instead of diagonally
    def next_move(self, dirs, d): # d: direction to move
        if d % 2 != 0 and dirs == 8:
            self.dist = self.dist + 14
        else:
            self.dist = self.dist + 10
            
    # Estimation function for the remaining distance to the goal.
    def estimation(self, x_dest, y_dest):
        dx = x_dest - self.x
        dy = y_dest - self.y
        # Manhattan distance
        d = abs(dx) + abs(dy)
        return d

# A-star algorithm.
# The path returned will be a string of digits of directions.
def a_star(dx, dy, ax, ay, bx, by, hor, ver, dirs, the_map):
    row = hor * [0] 
    dir_map = [] # map of dirs
    closed_nodes = [] # map of closed nodes
    open_nodes = [] # map of open nodes

    for i in range(ver): # create 2d arrays
        closed_nodes.append(list(row))
        open_nodes.append(list(row))
        dir_map.append(list(row))

    pq = [[], []] # priority queues of open (not-yet-tried) nodes
    pq_index = 0 # priority queue index
    
    # create the start node and push into list of open nodes
    n0 = node(ax, ay, 0, 0)
    n0.update_pr(bx, by)
    heappush(pq[pq_index], n0)
    open_nodes[ay][ax] = n0.pr # mark it on the open nodes map

    # A* search
    while len(pq[pq_index]) > 0:
        # get the current node w/ the highest priority
        # from the list of open nodes
        n1 = pq[pq_index][0] # top node
        n0 = node(n1.x, n1.y, n1.dist, n1.pr)
        x = n0.x
        y = n0.y
        heappop(pq[pq_index]) # remove the node from the open list
        open_nodes[y][x] = 0
        closed_nodes[y][x] = 1 # mark it on the closed nodes map

        # quit searching when the goal is reached
        # if n0.estimate(xB, yB) == 0:
        if y == by and x == bx:
            # generate the path from finish to start
            # by following the dirs
            path = ''
            while not (y == ay and x == ax):
                j = dir_map[y][x]
                c = str((j + dirs / 2) % dirs)
                path = c + path
                x = x + dx[j]
                y = y + dy[j]
            return path

        # generate moves (child nodes) in all possible dirs
        for i in range(dirs):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > hor - 1 or ydy < 0 or ydy > ver - 1
                    or the_map[ydy][xdx] == 1 or closed_nodes[ydy][xdx] == 1):
                # generate a child node
                m0 = node(xdx, ydy, n0.dist, n0.pr)
                m0.next_move(dirs, i)
                m0.update_pr(bx, by)
                if open_nodes[ydy][xdx] > m0.pr:
                    # update the priority
                    open_nodes[ydy][xdx] = m0.pr
                    # update the parent direction
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pq_index][0].x == xdx and pq[pq_index][0].y == ydy):
                        heappush(pq[1 - pq_index], pq[pq_index][0])
                        heappop(pq[pq_index])
                    heappop(pq[pq_index]) # remove the target node
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pq_index]) > len(pq[1 - pq_index]):
                        pq_index = 1 - pq_index
                    while len(pq[pq_index]) > 0:
                        heappush(pq[1-pq_index], pq[pq_index][0])
                        heappop(pq[pq_index])       
                    pq_index = 1 - pq_index
                    heappush(pq[pq_index], m0) # add the better node instead
                # if it is not in the open list then add into that
                elif open_nodes[ydy][xdx] == 0:
                    open_nodes[ydy][xdx] = m0.pr
                    heappush(pq[pq_index], m0)
                    # mark its parent node direction
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
    return '' # if no route found

dirs = 8 # number of possible directions to move on the map
if dirs == 4:
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
elif dirs == 8:
    dx = [1, 1, 0, -1, -1, -1, 0, 1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]

hor = 1000 # horizontal size of the map
ver = 1000 # vertical size of the map
the_map = []
row = [0] * hor
for i in range(ver): # create empty map
    the_map.append(list(row))

### fillout the map with a '+' pattern
##for x in range(hor / 8, hor * 7 / 8):
##    the_map[ver / 2][x] = 1
##for y in range(ver / 8, ver * 7 / 8):
##    the_map[y][hor / 2] = 1

string = "30_71_100_240_60_121_180_91_111_9001_2200_7801_"
string2 = ""
for i in range(500):
    string2 = string2 + string
string3 = string2[:-1]
matrix = receive_compressed_into_matrix(string3, 1000)

##for y in range(ver):
##    for x in range(hor):
##        print matrix[y][x],
##    print

# randomly select start and finish locations from a list
sf = []
sf.append((0, 0, hor - 1, ver - 1))
sf.append((0, ver - 1, hor - 1, 0))
sf.append((hor / 2 - 1, ver / 2 - 1, hor / 2 + 1, ver / 2 + 1))
sf.append((hor / 2 - 1, ver / 2 + 1, hor / 2 + 1, ver / 2 - 1))
sf.append((hor / 2 - 1, 0, hor / 2 + 1, ver - 1))
sf.append((hor / 2 + 1, ver - 1, hor / 2 - 1, 0))
sf.append((0, ver / 2 - 1, hor - 1, ver / 2 + 1))
sf.append((hor - 1, ver / 2 + 1, 0, ver / 2 - 1))
(ax, ay, bx, by) = random.choice(sf)

print 'Map size (X, Y): ', hor, ver
print 'Start point: ', ax, ay
print 'Finish point: ', bx, by
t = time.time()
route = a_star(dx, dy, ax, ay, bx, by, hor, ver, dirs, the_map)
print 'Time used for determining the route (seconds): ', time.time() - t
print 'Route:'
print route

# mark the route on the map
if len(route) > 0:
    y = ay
    x = ax
    the_map[y][x] = 2
##    matrix[y][x] = 2
    for i in range(len(route)):
        j = int(route[i])
        x = x + dx[j]
        y = y + dy[j]
        the_map[y][x] = 3
##        matrix[y][x] = 3
    the_map[y][x] = 4
##    matrix[y][x] = 4

# display the map with the route added
##print 'Map:'
##for y in range(ver):
##    for x in range(hor):
####        xy = the_map[y][x]
##        xy = matrix[y][x]
##        if xy == 0:
##            print '.', # space
##        elif xy == 1:
##            print 'O', # obstacle
##        elif xy == 2:
##            print 'S', # start
##        elif xy == 3:
##            print 'R', # route
##        elif xy == 4:
##            print 'F', # finish
##    print

raw_input('Press Enter...')
