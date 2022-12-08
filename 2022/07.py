#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def count(current):
    sums_all = 0
    dir_sizes = []

    for d in set(current["dirs"].keys()) - {"..", "/"}:
        tmp, tmp_sizes = count(current["dirs"][d])
        sums_all += tmp
        dir_sizes.extend(tmp_sizes)

    # current directory
    dir_sizes.append(sums_all+current["file_sizes"])
    return sums_all+current["file_sizes"], dir_sizes


def main():

    lines = open_data("07.data")

    root = {"dirs": {"..": None, "/": None}, "file_sizes": 0}
    root["dirs"]["/"] = root
    current = root

    for l in lines:
        if l.startswith("$"):
            cmd = l.split(" ")
            if cmd[1] == "cd":
                if cmd[2] not in current["dirs"]:
                    current["dirs"][cmd[2]] = {"dirs": {"..": current, "/": root}, "file_sizes": 0}
                current = current["dirs"][cmd[2]]
        elif (t := l.split(" ")) and t[0] != "dir":
            current["file_sizes"] += int(t[0])

    size_all, sizes = count(root)
    print(sum(filter(lambda x: x <= 100000, sizes)))
    print(next(filter(lambda x: x >= 30000000 - (70000000 - size_all), sorted(sizes))))


if __name__ == "__main__":
    main()

# year 2022
# solution for 07.01: 1307902
# solution for 07.02: 7068748
