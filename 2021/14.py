#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data_groups("14.data")

    template = lines[0][0]
    rules = lmap(lambda x: tuple(x.split(" -> ")), lines[1])

    points = defaultdict(int, Counter(template))
    next_rules = defaultdict(int)
    for i in range(1,len(template)):
        next_rules[template[i-1]+template[i]] += 1

    rules = dict(rules)
    for i in range(40):
        if i == 10:
            print(max(points.values())-min(points.values()))
        _next_rules = defaultdict(int)
        for r, c in next_rules.items():
            points[rules[r]] += c

            _next_rules[r[0]+rules[r]] += c
            _next_rules[rules[r]+r[1]] += c

        next_rules = _next_rules

    print(max(points.values())-min(points.values()))


if __name__ == "__main__":
    main()

# year 2021
# solution for 14.01: 2947
# solution for 14.02: 3232426226464
