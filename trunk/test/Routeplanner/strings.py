import math

# Method to compress a matrix into a string.
def compress_matrix(matrix):
    how_many = 1
    old_value = -1
    string = ""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                if matrix[i][j] == old_value:
                    how_many = how_many + 1
                elif matrix[i][j] != old_value:
                    string = string + "_" + str(how_many) + "1"
                    how_many = 1
            elif matrix[i][j] == 1:
                if matrix[i][j] == old_value:
                    how_many = how_many + 1
                elif matrix[i][j] != old_value:
                    string = string + "_" + str(how_many) + "0"
                    how_many = 1
            old_value = matrix[i][j]
    return string

# Method to decompress the string into a matrix.
def receive_compressed_into_matrix(string, row_length):
    index = 0
    count = 0
    row_number = 0
    matrix = []
    line = []
    string = string.split('_')
    for i in range(len(string)):
        how_many = string[i][:-1]
        value = string[i][len(string[i]) - 1]
        how_many = int(how_many)
        value = int(value)
        for k in range(how_many):
            line.append(value)
        count += how_many
        count %= row_length
        if count == 0:
            matrix.append(line)
            line = []
    return matrix

##def create_int_matrix(matrix):
##    x , y = matrix.shape
##    for i in range (x):
##        for j in range (y):
##             = matrix[i][j]
            
##string = "5001_5000_"
##string2 = "" 
##for i in range(1000):
##    string2 = string2 + string
##string2 = string2[:-1]
##test = receive_compressed_into_matrix(string2, 1000)
##print test
##print compress_matrix(test)

##string2 = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111100000000000000000000000000000000000000000000000001111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000000000000000000000000000000000000000000000000000000000001000000000010101010101010100010101010101000000000000000000000111111111111"
##string3 = ""
##for i in range(1000):
##    string3 = string3 + string2
##test2 = divide_string(string3, 999, 1000)
##matrix = create_matrix(test2)
##downsized_matrix = downsize_matrix(matrix)
##
##print len(downsized_matrix)
##
##print 'Map:'
##for y in range(200):
##    for x in range(200):
##        xy = downsized_matrix[y][x]
##        if xy == '1':
##            print '.', # space
##        elif xy == '0':
##            print 'O', # obstacle



