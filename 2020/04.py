#!/usr/bin/env python3.7

from utility import *
import re

def is_valid(s):
    if not all(x in s for x in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]):
        return False, False

    try:
        for k in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:
            v = s[k]

            if k == "byr" and not (1920 <= int(v) <= 2002):
                return True, False
            if k == "iyr" and not (2010 <= int(v) <= 2020):
                return True, False
            if k == "eyr" and not (2020 <= int(v) <= 2030):
                return True, False

            if k == "hgt":
                m = re.match(r"(\d+)(cm|in)", v)
                if not m:
                    return True, False
                if m.group(2) == "cm" and not (150 <= int(m.group(1)) <= 193):
                    return True, False
                if m.group(2) == "in" and not (59 <= int(m.group(1)) <= 76):
                    return True, False
            if k == "hcl" and not re.match(r"(#(\d|[a-f]){6})$", v):
                return True, False
            if k == "ecl" and v not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                return True, False
            if k == "pid" and not re.match(r"\d{9}$", v):
                return True, False

    except:
        return True, False

    return True, True

def main():

    lines = open_data("04.data", no_filter=True)
    # So we don't miss the last passport without an empty line after
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

    print(*valid)


if __name__ == "__main__":
    main()

# solution for 04.01: 254
# solution for 04.02: 184
