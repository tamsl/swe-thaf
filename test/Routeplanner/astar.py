import time
import random
import math
from heapq import *
from readmap import * 

class node:
    # priority = distance + est. remaining distance.
    pr = 0 
    dist = 0
    x = 0
    y = 0
    
    # Method used for initialization.
    def __init__(self, pr, dist, x, y):
        self.pr = pr
        self.dist = dist
        self.x = x
        self.y = y
        
    # Method for comparising priority queue.
    def __lt__(self, some): 
        if self.pr >= some.pr:
            return 0
        else:
            return 1

    # Method to determine an estimation for the remaining distance to end point.
    def manhattan(self, xf, yf):
        # Manhattan distance
        dy = yf - self.y
        dx = xf - self.x
        return abs(dy) + abs(dx)

    def new_pr(self, xf, yf):
        self.pr = 10 * self.manhattan(xf, yf) + self.dist 

    # Priority is given to going straight instead of in a diagonal way.
    def move(self, direction, directions):
        if directions != 8 and direction % 2 == 0:
            self.dist = 10 + self.dist
        else:
            self.dist = 14 + self.dist
        
# The actual A* search algorithm.
def a_star_search(dx, dy, xs, ys, xf, yf, xaxis, yaxis, directions, one_map):
    row = xaxis * [0] 

    # Map of directions
    drct_one_map = []
    # Index of the priority queue prq.
    index = 0
    # Priority queue of nodes that have not been tried (so open).
    prq = [[], []]
    # Map of open nodes
    n_open = []
    # Map of closed nodes 
    n_closed = []
    # Route, initialize as empty string
    route = ""

    for i in range(yaxis):
        drct_one_map.append(list(row))
        n_open.append(list(row))
        n_closed.append(list(row))

    # Node of start point is generated and pushed into the open nodes list.
    sn = node(0, 0, xs, ys)
    sn.new_pr(xf, yf)
    heappush(prq[index], sn)
    # Marked
    n_open[ys][xs] = sn.pr

    # Let's search.
    while 0 < len(prq[index]):
        # Receive the node containing the highest priority from the open nodes list.
        n1 = prq[index][0]
        sn = node(n1.pr, n1.dist, n1.x, n1.y)
        heappop(prq[index])
        y = sn.y
        x = sn.x
        # Marked
        n_closed[y][x] = 1
        n_open[y][x] = 0

        # In case destination is reached, stop the search.
        # The route is created from start point to end point.
        if xf == x:
            if yf == y:
                while not (ys == y and xs == x):
                    r = str((directions / 2 + drct_one_map[y][x]) % directions)
		    temp = drct_one_map[y][x]
         	    y = y + dy[temp]
                    x = x + dx[temp]
                    route = r + route
                return route

        # Creation of child nodes.
        for i in range(directions):
            dyy = dy[i] + y
            dxx = dx[i] + x
            if not (dxx < 0 or dxx > xaxis - 1 or dyy < 0 or dyy > yaxis - 1 or
                    n_closed[dyy][dxx] == 1 or one_map[dyy][dxx] == 1):
                cn = node(sn.pr, sn.dist, dxx, dyy)
                cn.move(i, directions)
                cn.new_pr(xf, yf)
                if cn.pr < n_open[dyy][dxx]:
                    n_open[dyy][dxx] = cn.pr
                    drct_one_map[dyy][dxx] = (directions / 2 + i) % directions
                    # Replace node. The node to be replaced it ignores and the new
                    # node shall be pushed in its place.
                    while not (dyy == prq[index][0].y and dxx == prq[index][0].x):
                        heappop(prq[index])
                        heappush(prq[1 - index], prq[index][0])
                    heappop(prq[index])
                    if len(prq[1 - index]) < len(prq[index]):
                        index = 1 - index
                    while len(prq[index]) != 0 and len(prq[index]) > 0:
                        heappop(prq[index])  
                        heappush(prq[1 - index], prq[index][0])
                    index = 1 - index
                    heappush(prq[index], cn)
                # In case it's not in the list of open nodes
                elif n_open[dyy][dxx] == 0:
                    heappush(prq[index], cn)
                    n_open[dyy][dxx] = cn.pr
                    drct_one_map[dyy][dxx] = (directions / 2 + i) % directions
    # Return emptry string, because no route was found.
    return ""

# Mark the route on the map.
def route_on_map(one_map, route, xs, ys):
    if len(route) > 0:
        y = ys
        x = xs
        one_map[y][x] = 2
        for i in range(len(route)):
            k = int(route[i])
            y = dy[k] + y
            x = dx[k] + x
            one_map[y][x] = 3
        one_map[y][x] = 4
    return one_map

# Print the map.
def show_map(one_map, xaxis, yaxis, print_msg):
    print '\n' + print_msg
    for y in range(yaxis):
        for x in range(xaxis):
            xy = one_map[y][x]
            if xy == 0:
                # Space
                print '.',
            elif xy == 1:
                # Obstacle
                print '#', 
            elif xy == 2:
                # Start
                print 'S', 
            elif xy == 3:
                # Route
                print 'R', 
            elif xy == 4: 
                # Finish
                print 'F', 
        print

one_map = []
xaxis = 60
yaxis = 60
row = xaxis * [0]
# Generate an empty map.
for i in range(yaxis): 
    one_map.append(list(row))

# Create start and finish points in a random way from a list.
points = []
points.append((0, 0, xaxis - 2, yaxis - 2))
points.append((0, yaxis - 2, xaxis - 3, 0))
points.append((0, yaxis / 2 - 2, xaxis - 1, yaxis / 3 + 2))
points.append((xaxis - 1, yaxis / 2 + 2, 0, yaxis / 3 - 2))
xs, ys, xf, yf = random.choice(points)

# Insert obstacles in the form of a '+' pattern.
for x in range(xaxis / 8, 7 * xaxis / 8):
    one_map[yaxis / 2][x] = 1
for y in range(yaxis / 8, 7 * yaxis / 8):
    one_map[y][xaxis / 2] = 1

# Number of possible directions.
directions = 8 
if directions == 8:
    dx = [1, 1, 0, -1, -1, -1, 0, 1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]
elif directions == 4:
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

route = a_star_search(dx, dy, xs, ys, xf, yf, xaxis, yaxis, directions, one_map)
print '\nSize of map: ', xaxis, yaxis
# Show the map without any route.
show_map(one_map, xaxis, yaxis, "Map without route:")
print '\nStart point: ', xs, ys
print 'Finish point: ', xf, yf

# Route shown on the map.
one_map = route_on_map(one_map, route, xs, ys)

# Show the map with the route included.
show_map(one_map, xaxis, yaxis, "Map with route included:")

# Show the important route points.
print '\n', read_map(one_map)
