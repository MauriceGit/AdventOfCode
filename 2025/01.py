#!/usr/bin/env python3

import sys

sys.path.append("../General")
from utility import *


def main():

    lines = lmap(lambda x: int(x[1:]) * (-1 if x[0] == "L" else 1), open_data("01.data"))

    n = 50
    p1, p2 = 0, 0
    for count in lines:
        f1 = abs(count) // 100
        f2 = abs(count) - f1*100
        p2 += f1 + (0 < (n if count < 0 else 100-n) <= f2)
        n = (n + count) % 100
        p1 += n == 0
    print(p1)
    print(p2)


if __name__ == "__main__":
    main()

# year 2025
# solution for 01.01: 1182
# solution for 01.02: 6907
