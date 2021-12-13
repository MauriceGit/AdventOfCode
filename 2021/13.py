#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def fold(paper, fold):

    fold_line = ints(fold)[0]
    fold_i = 0 if "x" in fold else 1
    lu = set(lfilter(lambda x: x[fold_i] <= fold_line, paper))
    rd = set(lfilter(lambda x: x[fold_i] >  fold_line, paper))

    tmp = set()
    for s in rd:
        new_x = s[0] if fold_i == 1 else fold_line-(s[0]-fold_line)
        new_y = s[1] if fold_i == 0 else fold_line-(s[1]-fold_line)
        tmp.add((new_x, new_y))

    return tmp | lu


def run_folds(paper, folds):

    for f in folds:
        paper = fold(paper, f)

    draw({k:1 for k in paper}, symbols={-1: " ", 1: "█"})


def main():

    dots, folds = open_data_groups("13.data")
    paper = {tuple(ints(d)) for d in dots}

    print(len(fold(paper, folds[0])))
    run_folds(paper, folds)


if __name__ == "__main__":
    main()

# year 2021
# solution for 13.01: 814
# solution for 13.02: PZEHRAER
