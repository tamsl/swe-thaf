#!/usr/bin/env python

import math
 
# Method to compress a matrix into a string.
def compress_matrix(matrix):
    how_many = 0
    old_value = -1
    string = ""
    # ---
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                if matrix[i][j] == old_value or (matrix[i][j] != old_value and i == 0 and j == 0):
                    how_many = how_many + 1
                elif matrix[i][j] != old_value:
                    if string == "":
                        string = str(how_many) + "1"
                    else:
                        string = string + "_" + str(how_many) + "1"
                    how_many = 1
            elif matrix[i][j] == 1:
                if matrix[i][j] == old_value or (matrix[i][j] != old_value and i == 0 and j == 0):
                    how_many = how_many + 1            
                elif matrix[i][j] != old_value:
                    if string == "":
                        string = str(how_many) + "0"
                    else:
                        string = string + "_" + str(how_many) + "0"
                    how_many = 1
            old_value = matrix[i][j]
 
    # The last number of values.
    if old_value == '0':
        string = string + "_" + str(how_many) + "1"
    else:
        string = string + "_" + str(how_many) + "0"
    return string
 
# Method to decompress the string into a matrix.
def decompress_string(string, row_length):
    index = 0
    count = 0
    row_number = 0
    matrix = []
    line = []
    string = string.split('_')
    # ---
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
 
# Test both methods on their functionality.            
partial = "5001_5000_"
string = ""
 
# Generate a string that if decompressed a 1000 by 1000 matrix appears. 
for i in range(1000):
    string = string + partial
string = string[:-1]
 
# A 1000 by 1000 matrix results from a string that has been decompressed.
matrix = decompress_string(string, 1000)
 
# Compress that matrix to a string.
string2 = compress_matrix(matrix)
 
# Check if the string before decompression and compression equals the
# one after decompression and compression.
if string == string2:
    print "\nString and string2 are equal. The compress and decompress methods both work.\n"
else:
    print "\nString and string2 are not equal. The compress and decompress methods don't work.\n"
 
# Test again for another string.          
partial = "2001_2000_501_500_3001_2000_"
string = ""
 
# Generate a string that if decompressed a 1000 by 1000 matrix appears. 
for i in range(1000):
    string = string + partial
string = string[:-1]
 
# A 1000 by 1000 matrix results from a string that has been decompressed.
matrix = decompress_string(string, 1000)
 
# Compress that matrix to a string.
string2 = compress_matrix(matrix)
 
# Check if the string before decompression and compression equals the
# one after decompression and compression.
if string == string2:
    print "String and string2 are equal. The compress and decompress methods both work.\n"
else:
    print "String and string2 are not equal. The compress and decompress methods don't work.\n"
