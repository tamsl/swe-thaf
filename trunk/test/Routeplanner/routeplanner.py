import sys
import heapq
import copy

def Astar(start, goal):
##    closedset := the empty set    // The set of nodes already evaluated.
##    openset := set containing the initial node    // The set of tentative nodes to be evaluated.
##    came_from := the empty map    // The map of navigated nodes.
    closedset = []
    openset = [start]
    came_from = []
    
    g_score[start] = 0    #// Cost from start along best known path.
    h_score[start] = heuristic_cost_estimate(start, goal)
    f_score[start] = h_score[start]    #// Estimated total cost from start to goal through y.
 
    while len(openset) != 0:
        index_val = find_index_val(f_score)
        # the node in openset having the lowest f_score[] value
        x = openset[index_val]
        if x == goal:
            return reconstruct_path(came_from, came_from[goal])
 
        ivalue = openset.index(x)
        # remove x from openset
        openset.pop(ivalue)
        # add x to closedset
        closedset.append(x)
        for y in neighbor_nodes(x):
            if y in closedset:
                 continue
            tentative_g_score = g_score[x] + dist_between(x,y)

            if y in openset:
                tentative_is_better = false
            elif tentative_g_score < g_score[y]:
                tentative_is_better = true
            else:
                openset.append(y)
                tentative_is_better = true

            if tentative_is_better == true:
                came_from[y] = x
                g_score[y] = tentative_g_score
                h_score[y] = heuristic_cost_estimate(y, goal)
                f_score[y] = g_score[y] + h_score[y]
 
    return "failure"
 
def reconstruct_path(came_from, current_node):
    if came_from[current_node] != NULL:
        p = reconstruct_path(came_from, came_from[current_node])
        return (p + current_node)
    else:
        return current_node

def find_index_val(to_be_sorted):
    sorted_to_be_sorted = sorted(to_be_sorted)
    index_val = to_be_sorted.index(sorted_to_be_sorted[0])
    return index_val

# manhattan method
def heuristic_cost_estimate(some_grid, goal):
    H = 10 * (abs(some_grid[0] - goal[0]) + abs(some_grid[1] - goal[1]))
    return H

def dist_between(x, y):
    return 1

def neighbor_nodes(x):
    return neighbors_x

while(1):
    start = [1.0, 2.0]
    goal = [4.0, 4.0]
    print heuristic_cost_estimate(start, goal)
