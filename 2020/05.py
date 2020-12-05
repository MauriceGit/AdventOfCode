#!/usr/bin/env python3.7

from utility import *

def main():

    lines = open_data("05.data")
    ids = set()

    for l in lines:
        row = int(l[:7].replace("B", "1").replace("F", "0"), 2)
        col = int(l[7:].replace("R", "1").replace("L", "0"), 2)

        ids.add(row*8+col)

    print(max(ids))
    print(*{x for x in range(128*8) if {x-1, x, x+1} & ids == {x-1, x+1}})


if __name__ == "__main__":
    main()

# solution for 05.01: 848
# solution for 05.02: 682
