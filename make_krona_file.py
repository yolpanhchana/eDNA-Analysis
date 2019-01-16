from collections import Counter
import sys

with open(sys.argv[1], 'r') as input_file:
    counts = Counter(input_file)
    with open("kronachart.txt", 'w') as output_file:
        for name, count in counts.most_common():
            output_file.write("%s\t%s" % (count, name))
    