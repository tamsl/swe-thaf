def read_map(matrix):
    route = []
    for i in range(len(matrix)):
        for k in range(len(matrix)):
            if matrix[i][k] == 'S':
                xs = i
                ys = k
            elif matrix[i][k] == 'F':
                xf = i
                yf = k 
    print "S", xs, ys
    print "F", xf, yf
    x = xs
    y = ys
    flag = 1
    new_angle = 0
    old_angle = -1
    route.append([x, y])
    while flag == 1:
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < x and j < y:
                    new_angle = 1
                elif i < x and j == y:
                    new_angle = 2
                elif i < x and j > y:
                    new_angle = 3
                elif i == x and j < y:
                    new_angle = 4
                elif i == x and j > y:
                    new_angle = 6
                elif i > x and j < y:
                    new_angle = 7
                elif i > x and j == y:
                    new_angle = 8
                elif i > x and j > y:
                    new_angle = 9
                if matrix[i][j] == 'R':
                    if i != x or j != y:
                        matrix[i][j] = 0
                        if old_angle == new_angle:
                            route.pop()
                        old_angle = new_angle
                        x = i
                        y = j
                        route.append([x, y])
                elif matrix[i][j] == 'F':
                    if old_angle == new_angle:
                       route.pop()
                    route.append([xf, yf])
                    flag = 0
    return route
    
matrix = [[0, 'R', 'R', 0, 0], ['R', 0, 0, 'R', 0], ['S', 0, 0, 'R', 0], [0, 0, 0, 'R', 0], [0, 0, 0, 'F', 0]]

## display the map with the route added
print 'Map:'
for y in range(len(matrix)):
    for x in range(len(matrix)):
        xy = matrix[y][x]
        if xy == 0:
            print '.', # space
        elif xy == 'S':
            print 'S', # start
        elif xy == 'R':
            print 'R', # route
        elif xy == 'F':
            print 'F', # finish
    print

print read_map(matrix)
