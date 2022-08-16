#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def clean_garbage(s):
    while "!" in s:
        i = s.index("!")
        s = s[:i] + s[i+2:]

    cancelled = 0
    while "<" in s:
        start = s.index("<")
        end = s.index(">", start)
        s = s[:start] + s[end+1:]
        cancelled += end-start-1

    return s, cancelled


def count_groups(stream, index, depth):
    score = depth
    i = index
    while i < len(stream):
        if stream[i] == "{":
            tmp_score, tmp_index = count_groups(stream, i+1, depth+1)
            i = tmp_index
            score += tmp_score
            continue
        if stream[i] == "}":
            return score, i+1
        i += 1
    return score, 0


def main():
    stream = open_data("09.data")[0]
    stream, cancelled = clean_garbage(stream)
    print(count_groups(stream, 0, 0)[0])
    print(cancelled)


if __name__ == "__main__":
    main()

# year 2017
# solution for 09.01: 16689
# solution for 09.02: 7982
