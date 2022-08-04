#!/usr/bin/env python3

import requests
from datetime import date
from datetime import timedelta
import browser_cookie3
import sys
import os


def setup_data(day, year):
    cookies = browser_cookie3.firefox()

    data_file = day + ".data"

    if os.path.isfile(data_file):
        return f"Data for day {day} already downloaded"

    r = requests.get(f"https://adventofcode.com/{year}/day/{int(day)}/input", cookies=cookies)

    with open(data_file, "w") as f:
        f.write(r.text)

    return ""

def setup_py(day, year):

    base_dir = os.path.dirname(os.path.realpath(__file__))
    py_file = day + ".py"

    if os.path.isfile(py_file):
        return f"Py for day {day} already exists"

    template = ""
    with open(base_dir + "/template.py", "r") as f:
        template = f.read()

    template = template.replace("[day]", day)
    template = template.replace("[year]", year)

    with open(py_file, "w") as f:
        # executable bit set, otherwise normal.
        os.chmod(py_file, 0o0775)
        f.write(template)

    return ""

# Without parameters, it downloads/setups the current day and year
# First argument is the day (if not today)
# Second argument is the year (if not this year)
if __name__ == "__main__":

    day  = date.today().strftime("%d")
    year = this_year = date.today().strftime("%Y")

    if len(sys.argv) > 1:
        day = "{:02d}".format(int(sys.argv[1]))
    if len(sys.argv) > 2:
        year = sys.argv[2]

    if not (0 < int(day) <= 25):
        exit(f"Invalid day: {day}")

    if not (2015 <= int(year) <= int(this_year)):
        exit(f"Invalid year: {year}")

    e1 = setup_data(day, year)
    e2 = setup_py(day, year)

    if e1 != "" or e2 != "":
        exit(e1 + "\n" + e2)
