#!/usr/bin/env python3.7

from utility import *

def main():

    lines = open_data("05.data")
    ids = set()

    for l in lines:
        id_ = l.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0")
        ids.add(int(id_[:7], 2)*8 + int(id_[7:], 2))

    print(max(ids))
    print(*{x for x in range(128*8) if {x-1, x, x+1} & ids == {x-1, x+1}})


if __name__ == "__main__":
    main()

# solution for 05.01: 848
# solution for 05.02: 682
