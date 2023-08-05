#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def main():

    btn_1 = (2,2)
    btn_2 = (1,3)
    sln_1 = ""
    sln_2 = ""
    f1 = ["00000",
          "01230",
          "04560",
          "07890",
          "00000"]
    f2 = ["0000000",
          "0001000",
          "0023400",
          "0567890",
          "00ABC00",
          "000D000",
          "0000000"]

    parse_field = lambda f: {(x,y):c for y,l in enumerate(f) for x,c in enumerate(l)}
    field_1 = parse_field(f1)
    field_2 = parse_field(f2)

    for l in open_data("02.data"):
        for c in l:
            d = direction_map()[c]
            btn_1 = add(btn_1, d) if field_1[add(btn_1, d)] != "0" else btn_1
            btn_2 = add(btn_2, d) if field_2[add(btn_2, d)] != "0" else btn_2

        sln_1 += str(field_1[btn_1])
        sln_2 += str(field_2[btn_2])

    print(sln_1)
    print(sln_2)

if __name__ == "__main__":
    main()

# year 2016
# solution for 02.01: 38961
# solution for 02.02: 46C92
