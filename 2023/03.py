#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("03.data")

    num_ok = lambda x: x != "." and not x.isnumeric()

    # *-pos -> [numbers]
    gears = defaultdict(list)

    final_sum = 0
    for i, line in enumerate(lines):
        numbers = ints(line)
        for n in numbers:
            n = n if n >= 0 else -n

            index = line.index(str(n))
            length = int(math.log10(n))+1
            line = line.replace(str(n), "0"*length, 1)

            ok = False
            positions = [(index-1, i), (index+length, i)]
            positions.extend(zip(range(index-1, index+length+1), [i-1]*(length+2)))
            positions.extend(zip(range(index-1, index+length+1), [i+1]*(length+2)))
            for pos in positions:
                if 0 <= pos[0] <= len(line)-1 and 0 <= pos[1] <= len(lines)-1 :
                    ok = ok or num_ok(lines[pos[1]][pos[0]])
                    if lines[pos[1]][pos[0]] == "*":
                        gears[pos].append(n)
            if ok:
                final_sum += n

    print(final_sum)
    print(sum(map(lambda x:x[0]*x[1], filter(lambda x: len(x) == 2, gears.values()))))


if __name__ == "__main__":
    main()

# year 2023
# solution for 03.01: 553825
# solution for 03.02: 93994191
