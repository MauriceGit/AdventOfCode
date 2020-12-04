#!/usr/bin/env python3.7

from utility import *
import re

def is_valid(s):
    if not all(x in s for x in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]):
        return False, False

    try:
        for k in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:
            v = s[k]

            if k == "byr" and (int(v) < 1920 or int(v) > 2002):
                return True, False
            if k == "iyr" and (int(v) < 2010 or int(v) > 2020):
                return True, False
            if k == "eyr" and (int(v) < 2020 or int(v) > 2030):
                return True, False
            if k == "hgt":
                if v[-2:] not in ["in", "cm"]:
                    return True, False
                v2 = int(v[:-2])
                if v[-2:] == "cm" and (v2 < 150 or v2 > 193):
                    return True, False
                elif v[-2:] == "in" and (v2 < 59 or v2 > 76):
                    return True, False

            if k == "hcl" and (v[0] != "#" or not re.match(r"(\d|[a-f]){6}", v[1:])):
                return True, False
            if k == "ecl" and v not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                return True, False
            if k == "pid" and not re.match(r"\d{9}", v):
                return True, False

    except:
        return True, False

    return True, True

def main():

    lines = open_data("04.data", no_filter=True)
    lines.append("")

    valid = (0,0)

    passport = dict()
    for i, l in enumerate(lines):

        if l == "":
            valid = add(valid, is_valid(passport))
            passport = dict()
            continue


        for l2 in l.split(" "):
            key, value = l2.split(":")
            passport[key] = value


    print(valid)



if __name__ == "__main__":
    main()

# solution for 04.01: ?
# solution for 04.02: ?
