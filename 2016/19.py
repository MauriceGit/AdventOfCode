#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# 01234 | 5
#   2 4 | 2
#   2   | 1
#
# 0123456789 | 10
# 0 2 4 6 8  |  5
#     4   8  |  2
#     4      |  1
#
# 0123456789abcdefghi | 19
#   2 4 6 8 a c e g i |  9
#       6   a   e   i |  4
#       6       e     |  2
#       6             |  1
#                                           Kandidate bleibt bei len()%2==0 und rutscht 1*steps weiter nach vorne sonst
#                                           Länge der Liste halbiert sich jedes Mal. Bei Gerader Anzahl //2 sonst
#                                           entweder auf oder abgerundet, abhängig davon, ob die letzte Runde gerade oder ungerade war
#                                           : Aufrunden, wenn letzte Runde gerade war. Sonst abrunden.
# 0123456789abcdefghijklmnopqrstuvwxyz      kandidate: 0    steps: 1  - 2**0 len: 36
# 0 2 4 6 8 a c e g i k m o q s u w y       kandidate: 0    steps: 2  - 2**1 len: 18
# 0   4   8   c   g   k   o   s   w         kandidate: 0    steps: 4  - 2**2 len: 9
#         8       g       o       w         kandidate: 2**3 steps: 8  - 2**3 len: 5
#         8               o                 kandidate: 2**3 steps: 16 - 2**4 len: 2
#         8                                 kandidate: 2**3

def run(n):

    reductions = 1
    candidate = 0

    while n > 1:
        last_n = n
        steps = 2**reductions
        if n%2 != 0:
            candidate = candidate+steps
        n = n//2
        reductions += 1

    return candidate+1


def main():

    n = int(open_data("19.data")[0])

    print(run(n))


if __name__ == "__main__":
    main()

# year 2016
# solution for 19.01: < 2877484, > 65572+1, != 1808356
# solution for 19.02: ?
