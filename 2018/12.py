#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *



def main():

    init, updates = open_data_groups("12.data")

    plants = [1 if e == '#' else 0 for e in init[0].split(": ")[1]]

    print(plants)




if __name__ == "__main__":
    main()

# year 2018
# solution for 12.01: ?
# solution for 12.02: ?
