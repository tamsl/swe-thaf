def read_map(matrix):
    route = []
    xs = 0
    ys = 0
    xf = 0
    yf = 0
    for i in range(len(matrix)):
        for k in range(len(matrix[i])):
            if matrix[i][k] == 2:
                xs = k
                ys = i
            elif matrix[i][k] == 4:
                xf = k
                yf = i 
    x = xs
    y = ys
    flag = 1
    new_angle = 0
    old_angle = -1
    route.append([x, y])
    while flag:
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if i >= 0 and j >= 0 and i < len(matrix) and j < len(matrix[i]):
                    if i < y and j < x:
                        new_angle = 1
                    elif i < y and j == x:
                        new_angle = 2
                    elif i < y and j > x:
                        new_angle = 3
                    elif i == y and j < x:
                        new_angle = 4
                    elif i == y and j > x:
                        new_angle = 6
                    elif i > y and j < x:
                        new_angle = 7
                    elif i > y and j == x:
                        new_angle = 8
                    elif i > y and j > x:
                        new_angle = 9
                    if matrix[i][j] == 3 and (new_angle % 2 == 1):
                        if new_angle == 1:
                            if matrix[y - 1][x] == 3:
                                new_angle = 2
                                if i != y or j != x:
                                    matrix[y - 1][x] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y - 1
                                    x = x
                                    route.append([x, y])
                            elif matrix[y][x - 1] == 3:
                                new_angle = 4
                                if i != y or j != x:
                                    matrix[y][x - 1] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y
                                    x = x - 1
                                    route.append([x, y])
                            else:
                                if i != y or j != x:
                                    matrix[i][j] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = i
                                    x = j
                                    route.append([x, y])
                        elif new_angle == 3:
                            if matrix[y - 1][x] == 3:
                                new_angle = 2
                                if i != y or j != x:
                                    matrix[y - 1][x] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y - 1
                                    x = x
                                    route.append([x, y])
                            elif matrix[y][x + 1] == 3:
                                new_angle = 6
                                if i != y or j != x:
                                    matrix[y][x + 1] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y
                                    x = x + 1
                                    route.append([x, y])
                            else:
                                if i != y or j != x:
                                    matrix[i][j] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = i
                                    x = j
                                    route.append([x, y])
                        elif new_angle == 7:
                            if matrix[y][x - 1] == 3:
                                new_angle = 4
                                if i != y or j != x:
                                    matrix[y][x - 1] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y
                                    x = x - 1
                                    route.append([x, y])                                    
                            elif matrix[y + 1][x] == 3:
                                new_angle = 8
                                if i != y or j != x:
                                    matrix[y + 1][x] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y + 1
                                    x = x
                                    route.append([x, y])
                            else:
                                if i != y or j != x:
                                    matrix[i][j] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = i
                                    x = j
                                    route.append([x, y])
                        elif new_angle == 9:
                            if matrix[y][x + 1] == 3:
                                new_angle = 6
                                if i != y or j != x:
                                    matrix[y][x + 1] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y
                                    x = x + 1
                                    route.append([x, y])
                            elif matrix[y + 1][x] == 3:
                                new_angle = 8
                                if i != y or j != x:
                                    matrix[y + 1][x] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y + 1
                                    x = x
                                    route.append([x, y])
                            else:
                                if i != y or j != x:
                                    matrix[i][j] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = i
                                    x = j
                                    route.append([x, y])    
                    elif matrix[i][j] == 3:
                        if i != y or j != x:
                            matrix[i][j] = 0
                            if old_angle == new_angle:
                                route.pop()
                            old_angle = new_angle
                            y = i
                            x = j
                            route.append([x, y])
                    elif matrix[i][j] == 4 and new_angle % 2 == 1:
                        if new_angle == 1:
                            if matrix[y - 1][x] == 3:
                                new_angle = 2
                                if i != y or j != x:
                                    matrix[y - 1][x] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y - 1
                                    x = x
                                    route.append([x, y])
                            elif matrix[y][x - 1] == 3:
                                new_angle = 4
                                if i != y or j != x:
                                    matrix[y][x - 1] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y
                                    x = x - 1
                                    route.append([x, y])
                            else:
                                if i != y or j != x:
                                    if matrix[i][j] == 4:
                                        if old_angle == new_angle:
                                           route.pop()
                                        route.append([xf, yf])
                                        flag = 0
                        elif new_angle == 3:
                            if matrix[y - 1][x] == 3:
                                new_angle = 2
                                if i != y or j != x:
                                    matrix[y - 1][x] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y - 1
                                    x = x
                                    route.append([x, y])
                            elif matrix[y][x + 1] == 3:
                                new_angle = 6
                                if i != y or j != x:
                                    matrix[y][x + 1] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y
                                    x = x + 1
                                    route.append([x, y])
                            else:
                                if i != y or j != x:
                                    if matrix[i][j] == 4:
                                        if old_angle == new_angle:
                                           route.pop()
                                        route.append([xf, yf])
                                        flag = 0
                        elif new_angle == 7:
                            if matrix[y][x - 1] == 3:
                                new_angle = 4
                                if i != y or j != x:
                                    matrix[y][x - 1] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y
                                    x = x - 1
                                    route.append([x, y])                                    
                            elif matrix[y + 1][x] == 3:
                                new_angle = 8
                                if i != y or j != x:
                                    matrix[y + 1][x] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y + 1
                                    x = x
                                    route.append([x, y])
                            else:
                                if i != y or j != x:
                                    if matrix[i][j] == 4:
                                        if old_angle == new_angle:
                                           route.pop()
                                        route.append([xf, yf])
                                        flag = 0
                        elif new_angle == 9:
                            if matrix[y][x + 1] == 3:
                                new_angle = 6
                                if i != y or j != x:
                                    matrix[y][x + 1] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y
                                    x = x + 1
                                    route.append([x, y])
                            elif matrix[y + 1][x] == 3:
                                new_angle = 8
                                if i != y or j != x:
                                    matrix[y + 1][x] = 0
                                    if old_angle == new_angle:
                                        route.pop()
                                    old_angle = new_angle
                                    y = y + 1
                                    x = x
                                    route.append([x, y])
                            else:
                                if i != y or j != x:
                                    if matrix[i][j] == 4:
                                        if old_angle == new_angle:
                                           route.pop()
                                        route.append([xf, yf])
                                        flag = 0
                    elif matrix[i][j] == 4:
                        if old_angle == new_angle:
                           route.pop()
                        route.append([xf, yf])
                        flag = 0
    return route
    
##matrix = [[0, 0, 3, 0, 1, 2], [3, 3, 0, 3, 1, 3], [4, 1, 0, 3, 1, 3], [1, 0, 0, 3, 1, 3], [0, 1, 1, 3, 1, 3], [0, 1, 1, 3, 3, 3]]
####matrix = [[0, 0, 0, 0, 2, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 1, 3, 0, 0, 0], [0, 0, 0, 0, 0, 1, 3, 0, 0, 0], [0, 0, 0, 0, 0, 1, 3, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 3, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 3, 0], [0, 0, 0, 0, 0, 1, 0, 3, 0, 0], [0, 0, 0, 0, 0, 1, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 0, 0, 0]]
####matrix = [[0, 3, 3, 3, 0, 3, 2], [3, 3, 0, 3, 0, 3, 0], [4, 0, 0, 3, 0, 3, 0], [0, 0, 0, 3, 0, 3, 0], [0, 0, 0, 3, 0, 3, 0], [0, 0, 0, 3, 3, 3, 0]]
##
#### display the map with the route added
##print 'Map:'
##for y in range(len(matrix)):
##    for x in range(len(matrix[y])):
##        xy = matrix[y][x]
##        if xy == 0:
##            print '.', # space
##        elif xy == 1:
##            print '#', # obstacle
##        elif xy == 2:
##            print 'S', # start
##        elif xy == 3:
##            print 'R', # route
##        elif xy == 4:
##            print 'F', # finish
##    print
##
##print read_map(matrix)
