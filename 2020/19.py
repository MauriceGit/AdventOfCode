#!/usr/bin/env python3.7

from utility import *

from cachetools import cached, LRUCache
from cachetools.keys import hashkey

cache = LRUCache(maxsize=10000)
@cached(cache, key=lambda rules, rule: hashkey(rule))
def combine_rules(rules, rule):

    if rule in "ab":
        return rule

    # handles: 223+
    if "+" in rule:
        return "(" + combine_rules(rules, rule[:-1]) + ")+"

    # handles: 223{3}
    if "{" in rule:
        reg = re.match(r"(\d+)\{(\d+)\}", rule)
        if reg:
            new_r = combine_rules(rules, reg.group(1))
            return "({}{{{}}})".format(new_r, reg.group(2))

    this_rule = rules[rule]
    tmp = this_rule.split(" | ")
    if len(tmp) > 1:

        res = ""
        for k in tmp:
            new_rules = k.split(" ")
            new_rules  = "".join(lmap(lambda x: combine_rules(rules, x), new_rules))

            if res != "":
                res += "|{}".format(new_rules)
            else:
                res += new_rules

        return "({})".format(res)

    return "".join(lmap(lambda x: combine_rules(rules, x), this_rule.split(" ")))


def main():

    rules_, data = open_data_groups("19.data")


    # "a" -> a
    rules_ = lmap(lambda x: x.replace("\"a\"", "a").replace("\"b\"", "b"), rules_)
    # dict of rules
    rules = dict({tuple(r.replace(": ", ":").split(":", 1)) for r in rules_})

    rule = "^" + combine_rules(rules, "0") + "$"
    print(len(list(filter(None.__ne__, lmap(lambda x: re.match(rule, x), data)))))

    # Clear cache, otherwise we just get the same result again :)
    cache.clear()

    # Those are the official replacements!
    #rules["8"]  = "42 | 42 8"
    #rules["11"] = "42 31 | 42 11 31"

    rules["8"] = "42+"
    rules["11"] = ""

    longest_line = max(lmap(len, data))
    # It just iterates twice. Larger values make it REALLY slow...
    longst_line = 2

    # Just put all possibilities up to the longest_line into the rules.
    for i in range(1, longest_line):

        rules["11_{}".format(i)] = "42{{{}}} 31{{{}}}".format(i, i)

        if rules["11"] != "":
            rules["11"] += " | "
        rules["11"] += "11_{}".format(i)

    rule = "^" + combine_rules(rules, "0") + "$"

    print(len(list(filter(None.__ne__, lmap(lambda x: re.match(rule, x), data)))))

if __name__ == "__main__":
    main()

# solution for 19.01: 239
# solution for 19.02: 405
