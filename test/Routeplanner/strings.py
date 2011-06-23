def receive_compressed(string):
    reg_string = ""
    string = string.split('_')
    for i in range(len(string)):
        string[i] = string[i].split('-')
        how_many = int(string[i][0])
        if string[i][1] == '1':
            for j in range(0, how_many):
                reg_string = reg_string + '1'
        elif string[i][1] == '0':
            for j in range(0, how_many):
                reg_string = reg_string + '0'
    return reg_string

def divide_string(string):
    new_string = ""
    m = 999
    for i in range(len(string)):
        new_string = new_string + string[i]
        if i == m:
            new_string = new_string + "*"
            m = m + 1000
    return new_string

def create_matrix(string):
    matrix = string.split('*')
    return matrix

def downsize_matrix(matrix):
    one_or_zero = 0
    count_zero = 0
    count_one = 0
    start_range_c = 0
    end_range_c = 4
    start_range_r = 0
    end_range_r = 0
    downsized_matrix = []
    t = 0
    v = 0
    w = 0

    while t < 200:
        for i in range(start_range_c, end_range_c):
            for j in range(start_range_r, end_range_r):
                val = matrix[i][j]
                if val == 0:
                    count_zero = count_zero + 1
                elif val == 1:
                    count_one = count_one + 1
        if start_range_r == 995 and end_range_r == 999:
            start_range_c =+ 5
            end_range_c =+ 5
        start_range_r =+ 5
        end_range_r =+ 5
        t =+ 1
        print "How many free zones: ", count_one
        print "How many obstacles: ", count_zero
        if count_one < count_zero:
            one_or_zero = 0
        elif count_one > count_zero:
            one_or_zero = 1
##        downsized_matrix[v][w] = one_or_zero
##        if w == 199:
##            v =+ 1
##        w =+ 1
        
    return downsized_matrix

                


##string = "3-0_7-1_10-0"
##test = receive_compressed(string)
##
string2 = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111100000000000000000000000000000000000000000000000001111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000000000000000000000000000000000000000000000000000000000001000000000010101010101010100010101010101000000000000000000000111111111111"
string3 = ""
for i in range(1000):
    string3 = string3 + string2
test2 = divide_string(string3)
matrix = create_matrix(test2)
downsized_matrix = downsize_matrix(matrix)

print 'Map:'
for y in range(200):
    for x in range(200):
        xy = downsized_matrix[y][x]
        if xy == '1':
            print '.', # space
        elif xy == '0':
            print 'O', # obstacle

##matrix = [[1, 1, 1, 1, 0],[0, 1, 1, 1, 1],[1, 0, 0, 0, 1],[1, 1, 1, 0, 0],[0, 0, 0, 0, 0]]
##print matrix
##print downsize_matrix(matrix)



