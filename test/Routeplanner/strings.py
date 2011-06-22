def receive_compressed(string):
    reg_string = ""
    print string
    string = string.split('_')
    print string
    for i in range(len(string)):
        string[i] = string[i].split('-')
        how_many = int(string[i][0])
        if string[i][1] == '1':
            for j in range(0, how_many):
                reg_string = reg_string + '1'
        elif string[i][1] == '0':
            for j in range(0, how_many):
                reg_string = reg_string + '0'
    print reg_string
    return reg_string

def divide_string(string):
    new_string = ""
    m = 999
    for i in range(len(string)):
        new_string = new_string + string[i]
        if i == m:
            new_string = new_string + "*"
            m = m + 1000
    print new_string
    print ""
    return new_string

def create_matrix(string):
    matrix = string.split('*')
    for i in range(len(matrix)):
        print matrix[i] + " "
        print ""
    return matrix

string = "3-0_7-1_10-0"
test = receive_compressed(string)

string2 = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111100000000000000000000000000000000000000000000000001111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000000000000000000000000000000000000000000000000000000000001000000000010101010101010100010101010101000000000000000000000111111111111"
string3 = ""
for i in range(1000):
    string3 = string3 + string2
print string3
test2 = divide_string(string3)
matrix = create_matrix(test2)

print 'Map:'
for y in range(1000):
    for x in range(1000):
        xy = matrix[y][x]
        if xy == '1':
            print '.', # space
        elif xy == '0':
            print 'O', # obstacle                  



