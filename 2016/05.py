#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

import hashlib

def main():

    door = open_data("05.data")[0]

    pw_1 = ""
    pw_2 = list("xxxxxxxx")
    count = 0

    md5 = hashlib.md5()
    md5.update(door.encode())

    for i in itertools.count():
        md5_ = md5.copy()
        md5_.update(str(i).encode())
        h = md5_.hexdigest()

        if h.startswith("00000"):
            if len(pw_1) < 8:
                pw_1 += h[5]
            if h[5].isdigit() and int(h[5]) < 8 and pw_2[int(h[5])] == "x":
                pw_2[int(h[5])] = h[6]
                count += 1
        if count == 8:
            break

    print(pw_1)
    print("".join(pw_2))


if __name__ == "__main__":
    main()

# year 2016
# solution for 05.01:
# solution for 05.02:
