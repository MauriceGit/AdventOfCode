#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

sall = 0
northpole_storage = 0

for l in open_data("04.data"):
    names = l.split("-")
    name = "".join(names[:-1])
    checksum = names[-1].split("[")[1][:-1]
    sid = int(names[-1].split("[")[0])

    common = sorted(Counter(name).most_common(), key=lambda x: (x[1], 26-ord(x[0])), reverse=True)
    if checksum == "".join(reduce(lambda x, y: x+y[0], common[:5], "")):
        sall += sid

    if "".join(map(lambda x: chr((ord(x)-ord('a') + sid)%26+97), names[0])) == "northpole":
        northpole_storage = sid

print(sall)
print(northpole_storage)
