#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def inflate(a, length):
    while len(a) < length:
        a = a + "0" + a[::-1].replace("0", "2").replace("1", "0").replace("2", "1")
    return a[:length]

def checksum(a):
    checksum = a
    while len(checksum)%2 == 0:
        a = checksum
        checksum = ""
        for i in range(0, len(a), 2):
            checksum += str(int(a[i] == a[i+1]))
    return checksum

def main():

    data = open_data("16.data")[0]
    print(checksum(inflate(data, 272)))
    print(checksum(inflate(data, 35651584)))


if __name__ == "__main__":
    main()

# year 2016
# solution for 16.01: 10111110010110110
# solution for 16.02: 01101100001100100
