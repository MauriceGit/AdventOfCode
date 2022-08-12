#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

Prog = namedtuple("Prog", "weight children")

def find_bottom(progs):
    all_children = set(chain.from_iterable(p.children for p in progs.values()))
    for name, p in progs.items():
        if len(p.children) > 0 and name not in all_children:
            return name


def calc_weight(p, progs):
    return progs[p].weight + sum(calc_weight(c, progs) for c in progs[p].children)


# returns: is_balanced, wrong_node, weight_diff
# weights: [(name, weight)]
def check(weights, progs):
    c = Counter(t[1] for t in weights)
    if len(c) <= 1:
        return True, "", 0

    wrong_node = next(name for (name,weight) in weights if weight == c.most_common()[1][0])
    return False, wrong_node, c.most_common()[1][0] - c.most_common()[0][0]


def verify_weights(p, progs, weight_diff):

    weights = []
    for c in progs[p].children:
        weights.append((c, calc_weight(c, progs)))

    is_balanced, wrong_node, diff = check(weights, progs)
    if not is_balanced:
        return verify_weights(wrong_node, progs, diff)

    return progs[p].weight - weight_diff


def parse(l):
    children = [] if "->" not in l else l.split("-> ")[1].split(", ")
    return l.split(" ")[0], Prog(ints(l)[0], children)


def main():

    lines = open_data("07.data")

    progs = dict(lmap(parse, lines))

    bottom = find_bottom(progs)
    print(bottom)
    print(verify_weights(bottom, progs, 0))


if __name__ == "__main__":
    main()

# year 2017
# solution for 07.01: mkxke
# solution for 07.02: 268
