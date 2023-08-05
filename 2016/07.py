#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def has_abba(s):
    for i in range(len(s)-3):
        if s[i] == s[i+3] and s[i+1] == s[i+2] and s[i] != s[i+1]:
            return True
    return False

# can not contain an abba in c
def check_abba(ok, not_ok=""):
    return has_abba(ok), has_abba(not_ok)

def find_abas(s, rev=False):
    abas = set()
    for i in range(len(s)-2):
        if s[i] == s[i+2] and s[i] != s[i+1]:
            abas.add(s[i:i+2] if not rev else s[i:i+2][::-1])
    return abas

def check_aba(outside, inside=""):
    return find_abas(outside), find_abas(inside, rev=True)

def main():

    lines = open_data("07.data")

    c1 = 0
    c2 = 0
    for l in lines:
        tmp = [check_abba(*s.split("[")) for s in l.split("]")]
        c1 += any(filter(lambda x: x[0], tmp)) and not any(filter(lambda x: x[1], tmp))

        tmp = [check_aba(*s.split("[")) for s in l.split("]")]
        good_abas = set().union(*map(lambda x: x[0], tmp))
        evil_abas = set().union(*map(lambda x: x[1], tmp))
        c2 += len(good_abas.intersection(evil_abas)) > 0

    print(c1)
    print(c2)


if __name__ == "__main__":
    main()

# year 2016
# solution for 07.01: 115
# solution for 07.02: 231
