#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def main():

    lines = [l.split(" ") for l in open_data("04.data")]

    print(sum(Counter(l).most_common()[0][1] == 1 for l in lines))

    lines = [[str(sorted(l2)) for l2 in l] for l in lines]
    print(sum(Counter(l).most_common()[0][1] == 1 for l in lines))


if __name__ == "__main__":
    main()

# year 2017
# solution for 04.01: 451
# solution for 04.02: 223
