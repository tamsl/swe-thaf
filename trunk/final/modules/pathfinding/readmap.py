def read_map(matrix):
    checkpoints = []
    xs = 0
    ys = 0
    xf = 0
    yf = 0
    
    # Find the coordinates for the start point and finish point.
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
    new_dir = 0
    old_angle = -1
    checkpoints.append([x, y])

    # In case finish point is not reached yet, keep going.
    while flag:
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if i >= 0 and j >= 0 and i < len(matrix) and j < len(matrix[i]):
                    # Determine the direction of the route.
                    # Consider a 3 by 3 square and fill it with the numbers 1 to 9
                    # and skip the 5. Those are the possible directions.
                    if i < y and j < x:
                        new_dir = 1
                    elif i < y and j == x:
                        new_dir = 2
                    elif i < y and j > x:
                        new_dir = 3
                    elif i == y and j < x:
                        new_dir = 4
                    elif i == y and j > x:
                        new_dir = 6
                    elif i > y and j < x:
                        new_dir = 7
                    elif i > y and j == x:
                        new_dir = 8
                    elif i > y and j > x:
                        new_dir = 9
                    # When a point of the route is found and the
                    # new direction is uneven (diagonal), you have to check
                    # if there is another route point in the vertical or
                    # horizontal direction.
                    if matrix[i][j] == 3 and new_dir % 2 == 1:
                        if new_dir == 1:
                            if matrix[y - 1][x] == 3:
                                new_dir = 2
                                if i != y or j != x:
                                    matrix[y - 1][x] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y - 1
                                    x = x
                                    checkpoints.append([x, y])
                            elif matrix[y][x - 1] == 3:
                                new_dir = 4
                                if i != y or j != x:
                                    matrix[y][x - 1] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y
                                    x = x - 1
                                    checkpoints.append([x, y])
                            else:
                                if i != y or j != x:
                                    matrix[i][j] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = i
                                    x = j
                                    checkpoints.append([x, y])
                        elif new_dir == 3:
                            if matrix[y - 1][x] == 3:
                                new_dir = 2
                                if i != y or j != x:
                                    matrix[y - 1][x] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y - 1
                                    x = x
                                    checkpoints.append([x, y])
                            elif matrix[y][x + 1] == 3:
                                new_dir = 6
                                if i != y or j != x:
                                    matrix[y][x + 1] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y
                                    x = x + 1
                                    checkpoints.append([x, y])
                            else:
                                if i != y or j != x:
                                    matrix[i][j] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = i
                                    x = j
                                    checkpoints.append([x, y])
                        elif new_dir == 7:
                            if matrix[y][x - 1] == 3:
                                new_dir = 4
                                if i != y or j != x:
                                    matrix[y][x - 1] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y
                                    x = x - 1
                                    checkpoints.append([x, y])                                    
                            elif matrix[y + 1][x] == 3:
                                new_dir = 8
                                if i != y or j != x:
                                    matrix[y + 1][x] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y + 1
                                    x = x
                                    checkpoints.append([x, y])
                            else:
                                if i != y or j != x:
                                    matrix[i][j] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = i
                                    x = j
                                    checkpoints.append([x, y])
                        elif new_dir == 9:
                            if matrix[y][x + 1] == 3:
                                new_dir = 6
                                if i != y or j != x:
                                    matrix[y][x + 1] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y
                                    x = x + 1
                                    checkpoints.append([x, y])
                            elif matrix[y + 1][x] == 3:
                                new_dir = 8
                                if i != y or j != x:
                                    matrix[y + 1][x] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y + 1
                                    x = x
                                    checkpoints.append([x, y])
                            else:
                                if i != y or j != x:
                                    matrix[i][j] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = i
                                    x = j
                                    checkpoints.append([x, y])
                    # When a point of the route is found and the
                    # new direction is even (vertical or horizontal),
                    # you do not have to check if there is another route point
                    # in the vertical or horizontal direction.
                    elif matrix[i][j] == 3:
                        if i != y or j != x:
                            matrix[i][j] = 0
                            # If the old direction and the new direction are equal.
                            # The last point in the check point array is not needed.
                            if old_angle == new_dir:
                                checkpoints.pop()
                            old_angle = new_dir
                            y = i
                            x = j
                            checkpoints.append([x, y])
                    # When the finish point is found and the new direction is
                    # uneven (diagonal), you have to check if there is another
                    # route point in the vertical or horizontal direction.
                    elif matrix[i][j] == 4 and new_dir % 2 == 1:
                        if new_dir == 1:
                            if matrix[y - 1][x] == 3:
                                new_dir = 2
                                if i != y or j != x:
                                    matrix[y - 1][x] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y - 1
                                    x = x
                                    checkpoints.append([x, y])
                            elif matrix[y][x - 1] == 3:
                                new_dir = 4
                                if i != y or j != x:
                                    matrix[y][x - 1] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y
                                    x = x - 1
                                    checkpoints.append([x, y])
                            else:
                                if i != y or j != x:
                                    if matrix[i][j] == 4:
                                        # If the old direction and the new direction are equal.
                                        # The last point in the check point array is not needed.
                                        if old_angle == new_dir:
                                           checkpoints.pop()
                                        checkpoints.append([xf, yf])
                                        # Change value of flag, the while loop quits.
                                        flag = 0
                        elif new_dir == 3:
                            if matrix[y - 1][x] == 3:
                                new_dir = 2
                                if i != y or j != x:
                                    matrix[y - 1][x] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y - 1
                                    x = x
                                    checkpoints.append([x, y])
                            elif matrix[y][x + 1] == 3:
                                new_dir = 6
                                if i != y or j != x:
                                    matrix[y][x + 1] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y
                                    x = x + 1
                                    checkpoints.append([x, y])
                            else:
                                if i != y or j != x:
                                    if matrix[i][j] == 4:
                                        # If the old direction and the new direction are equal.
                                        # The last point in the check point array is not needed.
                                        if old_angle == new_dir:
                                           checkpoints.pop()
                                        checkpoints.append([xf, yf])
                                        # Change value of flag, the while loop quits.
                                        flag = 0
                        elif new_dir == 7:
                            if matrix[y][x - 1] == 3:
                                new_dir = 4
                                if i != y or j != x:
                                    matrix[y][x - 1] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y
                                    x = x - 1
                                    checkpoints.append([x, y])                                    
                            elif matrix[y + 1][x] == 3:
                                new_dir = 8
                                if i != y or j != x:
                                    matrix[y + 1][x] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y + 1
                                    x = x
                                    checkpoints.append([x, y])
                            else:
                                if i != y or j != x:
                                    if matrix[i][j] == 4:
                                        # If the old direction and the new direction are equal.
                                        # The last point in the check point array is not needed.
                                        if old_angle == new_dir:
                                           checkpoints.pop()
                                        checkpoints.append([xf, yf])
                                        # Change value of flag, the while loop quits.
                                        flag = 0
                        elif new_dir == 9:
                            if matrix[y][x + 1] == 3:
                                new_dir = 6
                                if i != y or j != x:
                                    matrix[y][x + 1] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y
                                    x = x + 1
                                    checkpoints.append([x, y])
                            elif matrix[y + 1][x] == 3:
                                new_dir = 8
                                if i != y or j != x:
                                    matrix[y + 1][x] = 0
                                    # If the old direction and the new direction are equal.
                                    # The last point in the check point array is not needed.
                                    if old_angle == new_dir:
                                        checkpoints.pop()
                                    old_angle = new_dir
                                    y = y + 1
                                    x = x
                                    checkpoints.append([x, y])
                            else:
                                if i != y or j != x:
                                    if matrix[i][j] == 4:
                                        # If the old direction and the new direction are equal.
                                        # The last point in the check point array is not needed.
                                        if old_angle == new_dir:
                                           checkpoints.pop()
                                        checkpoints.append([xf, yf])
                                        # Change value of flag, the while loop quits.
                                        flag = 0
                    # When the finish point is found and the
                    # new direction is even (vertical or horizontal),
                    # you do not have to check if there is another route point
                    # in the vertical or horizontal direction.
                    elif matrix[i][j] == 4:
                        # If the old direction and the new direction are equal.
                        # The last point in the check point array is not needed.
                        if old_angle == new_dir:
                           checkpoints.pop()
                        checkpoints.append([xf, yf])
                        # Change value of flag, the while loop quits.
                        flag = 0
    return checkpoints
