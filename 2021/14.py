#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *
from collections import deque


def step(template, rules):
    count = len(template)
    for i in range(count-1):
        for r in rules:
            if template[0] == r[0][0] and template[1] == r[0][1]:
                template.rotate(-1)
                template.appendleft(r[1])
                template.rotate(1)
                break
        template.rotate(-2)
    template.rotate(-1)
    return template


def main():

    lines = open_data_groups("14.data")

    template = deque(lines[0][0])
    rules = lmap(lambda x: x.split(" -> "), lines[1])

    for i in range(15):
        template = step(template, rules)
        #print("".join(list(template)))
        #print()
        #print(Counter(template).items())
        s = sum(Counter(template).values())
        c = list(Counter(template).items())
        print(sorted(lmap(lambda x: (x[0], x[1]/s), c), key=lambda x: x[0]))
        print(max(Counter(template).values())-min(Counter(template).values()))


    c = Counter(template)
    print(c)
    print(max(c.values())-min(c.values()))




if __name__ == "__main__":
    main()

# year 2021
# solution for 14.01: ?
# solution for 14.02: ?
