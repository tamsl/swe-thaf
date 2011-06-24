def read_map(matrix):
    for i in range(len(matrix)):
        for k in range(len(matrix)):
            if matrix[i][k] == 'S':
                xs = i
                ys = k
            if matrix[i][k] == 'F':
                xf = i
                yf = k
            if matrix[i][k] == 'R':
                
    print "S", xs, ys
    print "F", xf, yf
    

matrix = [['S', 2, 3],['R', 5, 6],['R', 'R', 'F']]
print len(matrix)
read_map(matrix)

