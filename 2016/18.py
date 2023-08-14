#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def run(line, line_count):

    last_lines = [line.copy(), line.copy()]
    at = lambda l, i: "." if i<0 or i>=len(l) else l[i]
    save_count = sum(map(lambda x: 1 if x == "." else 0, line))

    for cc in range(line_count-1):
        last = last_lines[cc%2==0]
        curr = last_lines[cc%2==1]
        for i in range(len(last)):
            l, r = at(last, i-1), at(last, i+1)
            save_count += int(l==r)
            curr[i] = "." if l==r else "^"

    return save_count

def main():

    line = list(open_data("18.data")[0])
    print(run(line, 40))
    print(run(line, 400000))


if __name__ == "__main__":
    main()

# year 2016
# solution for 18.01: 1939
# solution for 18.02: 19999535
