#!/usr/bin/env python3.7

from utility import *

def get_removeable(lines):
    removeable = defaultdict(int)
    for i in reversed(range(2, len(lines))):
        if lines[i]-lines[i-1] < 3 and lines[i-1]-lines[i-2] < 3:
            removeable[lines[i-1]] = 1
    return list(removeable.keys())

def main():

    lines = sorted(ints(open_data("10.data")))

    diff = defaultdict(int)
    diff[lines[0]] = 1
    diff[3] = 1

    for i in range(1, len(lines)):
        diff[lines[i] - lines[i-1]] += 1


    print(diff[1]*diff[3])


    #removeable = defaultdict(int)
    #
    #for i in reversed(range(2, len(lines))):
    #    if lines[i]-lines[i-1] < 3 and lines[i-1]-lines[i-2] < 3:
    #        removeable[lines[i-1]] = 1



    l1 = get_removeable([0]+lines)

    print(get_removeable(lines))

    #l2 = get_removeable(sorted(l1))
    #print(get_removeable(sorted(l1)))

    print(2**len(l1))


if __name__ == "__main__":
    main()

# solution for 10.01: ?
# solution for 10.02: ?
