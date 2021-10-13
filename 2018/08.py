#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

# returns tuple of metadata-count and length of sub-data
def metadata_count(l):
    sub_length = 2
    res = 0

    for c in range(l[0]):
        a, b = metadata_count(l[sub_length:])
        res += a
        sub_length += b

    return res+sum(l[sub_length:sub_length+l[1]]), sub_length+l[1]

def main():

    line = ints(open_data("08.data")[0])

    print(metadata_count(line)[0])


if __name__ == "__main__":
    main()

# year 2018
# solution for 08.01: 40984
# solution for 08.02: ?
