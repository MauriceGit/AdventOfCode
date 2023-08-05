#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    columns = np.transpose(list(map(list, open_data("06.data"))))
    print("".join(Counter(c).most_common()[0][0] for c in columns))
    print("".join(Counter(c).most_common()[-1][0] for c in columns))


if __name__ == "__main__":
    main()

# year 2016
# solution for 06.01: mshjnduc
# solution for 06.02: apfeeebz
