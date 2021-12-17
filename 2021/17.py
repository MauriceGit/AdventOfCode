#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def verify_x(target_x, x_vel):
    x = 0
    steps = 0
    valid_steps = []
    while True:
        x += x_vel
        x_vel = max(0, x_vel-1)
        steps += 1
        if target_x[0] <= x <= target_x[1]:
            valid_steps.append(steps)
        if len(valid_steps) >= 1000 or x_vel == 0 and len(valid_steps) == 0 or x > target_x[1]:
            return valid_steps
    return []


def find_valid_x_velocities(target_x):
    valid_x = []
    for i in range(1000):
        valid_x.append((i, verify_x(target_x, i)))
    return valid_x


def verify_y(target_y, y_vel):
    y = 0
    steps = 0
    best_y = 0
    valid_steps = []
    while y >= target_y[0]:
        y += y_vel
        y_vel -= 1
        steps += 1
        best_y = max(best_y, y)
        if target_y[0] <= y <= target_y[1]:
            valid_steps.append(steps)
        if y < target_y[0]:
            return len(valid_steps) > 0, valid_steps, best_y
    return False, [], 0


def find_valid_y_velocities(target_y):
    valid_y = []
    for i in range(-500, 500):
        ok, steps, best_y = verify_y(target_y, i)
        if ok:
            valid_y.append((i, steps, best_y))
    return valid_y


def main():

    lines = open_data("17.data")
    tmp = ints(lines[0])
    target_area = ((tmp[0],tmp[1]), (tmp[2],tmp[3]))

    valid_x = find_valid_x_velocities(target_area[0])
    valid_y = find_valid_y_velocities(target_area[1])

    print(max(valid_y, key=lambda x:x[2])[2])

    all_valid = set()
    for x in valid_x:
        for x_steps in x[1]:
            for y in valid_y:
                for y_steps in y[1]:
                    if x_steps == y_steps:
                        all_valid.add((x[0],y[0]))
    print(len(all_valid))


if __name__ == "__main__":
    main()

# year 2021
# solution for 17.01: 2278
# solution for 17.02: 996
