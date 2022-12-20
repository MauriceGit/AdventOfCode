#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def mix(orig_numbers, numbers, number_mapping):
    for nn in orig_numbers:
        i = numbers.index(nn)
        numbers.rotate(-i)
        n = numbers.popleft()
        numbers.rotate(-number_mapping[nn])
        numbers.appendleft(n)
    return numbers

def get_solution(numbers, num_0, mapping):
    i = numbers.index(num_0)
    numbers.rotate(-i)
    return mapping[numbers[1000]]+mapping[numbers[2000]]+mapping[numbers[3000]]


def main():

    lines = open_data("20.data")
    num_0 = 0
    numbers = deque()
    number_mapping = dict()
    number_mapping2 = dict()
    for i, l in enumerate(lines):
        n = ints(l)[0]
        numbers.append(i)
        number_mapping[i] = n
        number_mapping2[i] = n*811589153
        if n == 0:
            num_0 = i

    p1n = mix(numbers, numbers.copy(), number_mapping)
    print(get_solution(p1n, num_0, number_mapping))

    orig_numbers = numbers.copy()
    for i in range(1):
        numbers = mix(orig_numbers, numbers, number_mapping2)
    print(get_solution(numbers, num_0, number_mapping2))


if __name__ == "__main__":
    main()

# year 2022
# solution for 20.01: 872
# solution for 20.02: 5382459262696
