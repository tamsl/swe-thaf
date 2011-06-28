def read_map(matrix):
    route = []
    xs = 0
    ys = 0
    xf = 0
    yf = 0
    for i in range(len(matrix)):
        for k in range(len(matrix)):
            if matrix[i][k] == 2:
                xs = i
                ys = k
            elif matrix[i][k] == 4:
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
    while flag:
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i >= 0 and j >= 0 and i < len(matrix) and j < len(matrix[i]):
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
                    if matrix[i][j] == 3 and (new_angle % 2 == 1):
                        if old_angle % 2 == 0:
                            if new_angle == 1:
                                if matrix[x - 1][y] == 3:
                                    new_angle = 2
                                    if i != x or j != y:
                                        matrix[x - 1][y] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = x - 1
                                        y = y
                                        route.append([x, y])
                                elif matrix[x][y - 1] == 3:
                                    new_angle = 4
                                    if i != x or j != y:
                                        matrix[x][y - 1] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = x
                                        y = y - 1
                                        route.append([x, y])
                                else:
                                    if i != x or j != y:
                                        matrix[i][j] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = i
                                        y = j
                                        route.append([x, y])
                            elif new_angle == 3:
                                if matrix[x - 1][y] == 3:
                                    new_angle = 2
                                    if i != x or j != y:
                                        matrix[x - 1][y] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = x - 1
                                        y = y
                                        route.append([x, y])
                                elif matrix[x][y + 1] == 3:
                                    new_angle = 6
                                    if i != x or j != y:
                                        matrix[x][y + 1] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = x
                                        y = y + 1
                                        route.append([x, y])
                                else:
                                    if i != x or j != y:
                                        matrix[i][j] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = i
                                        y = j
                                        route.append([x, y])
                            elif new_angle == 7:
                                if matrix[x][y - 1] == 3:
                                    new_angle = 4
                                    if i != x or j != y:
                                        matrix[x][y - 1] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = x
                                        y = y - 1
                                        route.append([x, y])                                    
                                elif matrix[x + 1][y] == 3:
                                    new_angle = 8
                                    if i != x or j != y:
                                        matrix[x + 1][y] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = x + 1
                                        y = y
                                        route.append([x, y])
                                else:
                                    if i != x or j != y:
                                        matrix[i][j] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = i
                                        y = j
                                        route.append([x, y])
                            elif new_angle == 9:
                                if matrix[x][y + 1] == 3:
                                    new_angle = 6
                                    if i != x or j != y:
                                        matrix[x][y + 1] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = x
                                        y = y + 1
                                        route.append([x, y])
                                elif matrix[x + 1][y] == 3:
                                    new_angle = 8
                                    if i != x or j != y:
                                        matrix[x + 1][y] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = x + 1
                                        y = y
                                        route.append([x, y])
                                else:
                                    if i != x or j != y:
                                        matrix[i][j] = 0
                                        if old_angle == new_angle:
                                            route.pop()
                                        old_angle = new_angle
                                        x = i
                                        y = j
                                        route.append([x, y])
                    elif matrix[i][j] == 3:
                        if i != x or j != y:
                            matrix[i][j] = 0
                            if old_angle == new_angle:
                                route.pop()
                            old_angle = new_angle
                            x = i
                            y = j
                            route.append([x, y])
                    elif matrix[i][j] == 4:
                        if old_angle == new_angle:
                           route.pop()
                        route.append([xf, yf])
                        flag = 0
    return route
    
##matrix = [[0, 3, 3, 3, 0, 2], [3, 3, 0, 3, 0, 3], [4, 0, 0, 3, 0, 3], [0, 0, 0, 3, 0, 3], [0, 0, 0, 3, 0, 3], [0, 0, 0, 3, 3, 3]]
##
#### display the map with the route added
##print 'Map:'
##for y in range(len(matrix)):
##    for x in range(len(matrix)):
##        xy = matrix[y][x]
##        if xy == 0:
##            print '.', # space
##        elif xy == 2:
##            print 'S', # start
##        elif xy == 3:
##            print 'R', # route
##        elif xy == 4:
##            print 'F', # finish
##    print
##
##print read_map(matrix)
