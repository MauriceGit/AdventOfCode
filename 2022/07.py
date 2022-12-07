#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def count(current):

    sums_all = 0
    sums_ok = 0
    dir_sizes = []

    for d in current["dirs"]:
        tmp, tmp_ok, tmp_sizes = count(d)
        if tmp <= 100000:
            #print(f"directory {current['name']} has size {tmp}")
            sums_ok += tmp
        sums_all += tmp
        sums_ok += tmp_ok
        dir_sizes.append(tmp)
        dir_sizes.extend(tmp_sizes)

    file_sum = 0
    for f in current["files"]:
        file_sum += f[1]
    #print("sums file", file_sum)

    #print("sums ok: ", sums_ok)

    return sums_all+file_sum, sums_ok, dir_sizes




def main():

    lines = open_data("07.data")

    root = {"..": None, "dirs": [], "files": [], "name": "/"}
    current = None
    # dir -> dict("..": up_dict, "dirs": [], "files": [])

    for l in lines:
        if l.startswith("$"):
            cmd = l.split(" ")
            if cmd[1] == "cd":
                if cmd[2] == "/":
                    current = root
                else:
                    if cmd[2] == "..":
                        current = current[".."]
                    else:
                        new_d = {"..": current, "dirs": [], "files": [], "name": cmd[2]}
                        current["dirs"].append(new_d)
                        current = new_d

            if cmd[1] == "ls":
                pass
        else:
            # list of files and sizes
            size, fd = l.split(" ")
            #print(f, size)
            if size == "dir":
                pass
            else:
                #current[2].append((fd, int(size)))
                current["files"].append((fd, int(size)))

    print(count(root)[1])
    size_all, _, sizes = count(root)

    to_delete = 70000000 - size_all
    sizes.sort()

    print(sizes)

    for s in sizes:
        if s >= to_delete:
            print("to_delete", s)
            break



    # not 24390891




if __name__ == "__main__":
    main()

# year 2022
# solution for 07.01: ?
# solution for 07.02: ?
