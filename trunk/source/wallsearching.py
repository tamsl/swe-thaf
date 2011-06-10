def min_sonar_val(sonar_vals):
    sorted_sonar_vals = sorted(sonar_vals)
    index_val = sonar_vals.index(sorted_sonar_vals[0])
    print sorted_sonar_vals[0]
    print index_val
    return sorted_sonar_vals[0], index_val
        
sonar_values = [4.001, 4.243, 5.000, 2.865, 3.852, 2.534, 1.948, 3.289]
min_val, index_val = min_sonar_val(sonar_values);
print min_val
print index_val
