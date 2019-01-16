import sys

with open(sys.argv[1], 'r') as input_file:
    significant_ones = []

    for line in input_file:
        percent_identity = float(line.split('\t')[2])
        base_pair = float(line.split('\t')[3])
        
        if percent_identity > 97 and base_pair > 200:
            significant_ones.append(line)
                
    significant_ones = sorted(significant_ones, 
        key=lambda(line): float(line.split('\t')[-1]))        
    
    for line in significant_ones:
        print(line.replace('\n', ''))