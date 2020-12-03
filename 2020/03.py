#!/usr/bin/env python3.7

from utility import *

def test(lines, s):

    length = len(lines[0])
    bottom = len(lines)
    count = 0
    pos = (0,0)
    while pos[1] < bottom:
        count += lines[pos[1]][pos[0]%length] == '#'
        pos = add(pos, s)

    return count

def main():

    lines = open_data("03.data")

    print(test(lines, (3,1)))

    count = 1
    count *= test(lines, (1,1))
    count *= test(lines, (3,1))
    count *= test(lines, (5,1))
    count *= test(lines, (7,1))
    count *= test(lines, (1,2))

    print(count)


if __name__ == "__main__":
    main()

# solution for 03.01: 232
# solution for 03.02: 3952291680
