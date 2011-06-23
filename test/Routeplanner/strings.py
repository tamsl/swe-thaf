def receive_compressed(string):
    reg_string = ""
    string = string.split('_')
    for i in range(len(string)):
        how_many = string[i][:-1]
        value = string[i][len(string[i]) - 1]
        how_many = int(how_many)
        value = int(value)
        if value == 1:
            for k in range(0, how_many):
                reg_string = reg_string + '1'
        elif value == 0:
            for k in range(0, how_many):
                reg_string = reg_string + '0'
    print reg_string
    return reg_string

def divide_string(string, m, step):
    new_string = ""
    for i in range(len(string)):
        new_string = new_string + string[i]
        if i == m:
            new_string = new_string + "*"
            m = m + step
    return new_string

def create_matrix(string):
    matrix = string.split('*')
    return matrix

def downsize_matrix(matrix):
    one_or_zero = ""
    count_zero = 0
    count_one = 0
    start_range_c = 0
    end_range_c = 5
    start_range_r = 0
    end_range_r = 5
    final_string = ""
    t = 0
    v = 0
    w = 0

    while t < 40000:
        for i in range(start_range_c, end_range_c):
            for j in range(start_range_r, end_range_r):
                val = float(matrix[i][j])
                if val == 0:
                    count_zero = count_zero + 1
                elif val == 1:
                    count_one = count_one + 1
##        print start_range_r, end_range_r
##        print start_range_c, end_range_c
##        print "How many free zones: ", count_one
##        print "How many obstacles: ", count_zero
        if (start_range_r == 995 and end_range_r == 1000) and (start_range_c < 995 and end_range_c < 1000):
            start_range_c = start_range_c + 5
            end_range_c = end_range_c + 5
            start_range_r = 0
            end_range_r = 5
        elif (start_range_r < 995 and end_range_r < 1000):
            start_range_r = start_range_r + 5
            end_range_r = end_range_r + 5
##        if (start_range_r == 995 and end_range_r == 1000) and (start_range_c == 995 and end_range_c == 1000):
##            print "DONE"
        if count_one < count_zero:
            one_or_zero = "0"
        elif count_one > count_zero:
            one_or_zero = "1"
        final_string = final_string + one_or_zero
        count_zero = 0
        count_one = 0
        t = t + 1
##        print t
    new_string = divide_string(final_string, 199, 200)
    downsized_matrix = create_matrix(new_string)
    # Because somehow the matrix has a length of 201.
    downsized_matrix.pop(200)
    return downsized_matrix

##string = "30_71_100_240_121_180_91"
##test = receive_compressed(string)
##
string2 = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111100000000000000000000000000000000000000000000000001111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000000000000000000000000000000000000000000000000000000000001000000000010101010101010100010101010101000000000000000000000111111111111"
string3 = ""
for i in range(1000):
    string3 = string3 + string2
test2 = divide_string(string3, 999, 1000)
matrix = create_matrix(test2)
downsized_matrix = downsize_matrix(matrix)

print len(downsized_matrix)

print 'Map:'
for y in range(200):
    for x in range(200):
        xy = downsized_matrix[y][x]
        if xy == '1':
            print '.', # space
        elif xy == '0':
            print 'O', # obstacle





