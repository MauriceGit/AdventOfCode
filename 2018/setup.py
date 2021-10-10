#!/usr/bin/env python3.7

import requests
from datetime import date
from datetime import timedelta
import browser_cookie3
import sys
import os

def setup_data(day):
    cookies = browser_cookie3.firefox()

    data_file = day + ".data"

    if os.path.isfile(data_file):
        return f"Data for day {day} already downloaded"

    r = requests.get(f"https://adventofcode.com/2018/day/{int(day)}/input", cookies=cookies)

    with open(data_file, "w") as f:
        f.write(r.text)

    return ""

def setup_py(day):

    py_file = day + ".py"

    if os.path.isfile(py_file):
        return f"Py for day {day} already exists"

    template = ""
    with open("template.py", "r") as f:
        template = f.read()

    template = template.replace("[day]", day)

    with open(py_file, "w") as f:
        # executable bit set, otherwise normal.
        os.chmod(py_file, 0o0775)
        f.write(template)

    return ""

if __name__ == "__main__":

    day = date.today().strftime("%d")

    if len(sys.argv) > 1:
        day = "{:02d}".format(int(sys.argv[1]))

    if not (0 < int(day) <= 25):
        exit(f"Invalid day: {day}")

    e1 = setup_data(day)
    e2 = setup_py(day)

    if e1 != "" or e2 != "":
        exit(e1 + "\n" + e2)
