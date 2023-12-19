#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


Workflow = namedtuple("Workflow", "rules default")
Rule = namedtuple("Rule", "check cmp num next_rule")

compare = {">": lambda part, p, num: part[p] > num, "<": lambda part, p, num: part[p] < num}


def is_accepted(workflows, part, state):
    if state == "A":
        return True
    if state == "R":
        return False

    for r in workflows[state].rules:
        if compare[r.cmp](part, r.check, r.num):
            return is_accepted(workflows, part, r.next_rule)
    return is_accepted(workflows, part, workflows[state].default)


# ranges: {"x": (0, 4000), "m": (0, 4000), ...}
# state starts with "in"
def count_accepted(workflows, state, ranges):
    if state == "R":
        return 0
    if state == "A":
        return reduce(operator.mul, map(lambda x: (x[1]+1)-x[0], ranges.values()))

    # check if our range does not get split by each rule! Only then we ignore it!
    for rule in workflows[state].rules:
        c = rule.check
        mi, ma = ranges[c]

        r_cpy1 = ranges.copy()
        r_cpy2 = ranges.copy()

        if rule.cmp == ">" and ma > rule.num:
            r_cpy1[c] = (rule.num+1, ma)
            r_cpy2[c] = (mi, rule.num)
            return count_accepted(workflows, rule.next_rule, r_cpy1) + count_accepted(workflows, state, r_cpy2)

        elif rule.cmp == "<" and mi < rule.num:
            r_cpy1[c] = (mi, rule.num-1)
            r_cpy2[c] = (rule.num, ma)
            return count_accepted(workflows, rule.next_rule, r_cpy1) + count_accepted(workflows, state, r_cpy2)

    return count_accepted(workflows, workflows[state].default, ranges)


def main():

    rules, part_list = open_data_groups("19.data")

    workflows = {"A": [], "R": []}
    parts = []

    for rule in rules:
        name = rule.split("{")[0]
        default = rule.split(",")[-1][:-1]
        l = []
        for r in rule.split("{")[1][:-1].split(",")[:-1]:
            p, compare, num, next_rule = re.findall(r"([a-z])([<>])(\d+):([ARa-z]+)", r)[0]
            l.append(Rule(p, compare, int(num), next_rule))
        workflows[name] = Workflow(l, default)

    for part in part_list:
        ns = lmap(int, *re.findall(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", part))
        parts.append(dict(list(zip("xmas", ns))))

    print(sum(is_accepted(workflows, part, "in") * sum(part.values()) for part in parts))

    print(count_accepted(workflows, "in", dict(zip("xmas", [(1,4000)]*4))))


if __name__ == "__main__":
    main()

# year 2023
# solution for 19.01: ?
# solution for 19.02: ?
