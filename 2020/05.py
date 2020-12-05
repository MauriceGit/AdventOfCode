#!/usr/bin/env python3.7

from utility import *

def main():

    ids = {int(l.translate("".maketrans("FBLR", "0101")), 2) for l in open_data("05.data")}

    print(max(ids), *{x for x in range(1024) if {x-1, x, x+1} & ids == {x-1, x+1}})


if __name__ == "__main__":
    main()

# solution for 05.01: 848
# solution for 05.02: 682
