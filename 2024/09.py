#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def get_space(spaces, minimum=1):
    index, count = 10000000000000000000, -1
    for i, h in enumerate(spaces):
        if i >= minimum and len(h) > 0 and h[0] < index:
            index, count = h[0], i
    if count == -1:
        return None, None
    return heappop(spaces[count]), count


def move(files, spaces, part2=False):
    last_insert = -1

    for src_index in sorted(list(files.keys()), reverse=True):

        file_id, file_count = files[src_index]

        while file_count > 0:
            space_index, space_count = get_space(spaces, minimum=file_count if part2 else 1)

            if space_index == None or space_index >= src_index:
                break

            # only copy parts of the file
            if space_count < file_count:
                files[space_index] = (file_id, space_count)
                files[src_index] = (file_id, file_count - space_count)
            else:
                # remove original file, potentially re-insert some space!
                del files[src_index]
                files[space_index] = (file_id, file_count)
                if space_count > file_count:
                    heappush(spaces[space_count-file_count], space_index+file_count)
            file_count = file_count - space_count
            last_insert = space_index


def checksum(files):
    checksum = 0
    for k in sorted(files.keys()):
        fid, count = files[k]
        for i in range(count):
            checksum += fid * (k+i)
    return checksum


def part1(files, spaces):
    files = files.copy()
    move(files, deepcopy(spaces))
    return checksum(files)


def part2(files, spaces):
    files = files.copy()
    move(files, deepcopy(spaces), part2=True)
    return checksum(files)


def main():

    line = open_data("09.data")[0]

    # index --> (id, count)
    files = dict()
    # list of min-heaps with free space indices corresponding to their index!
    spaces = []
    for i in range(10):
        spaces.append([])

    total_index = 0
    for i in range(0, len(line), 2):
        cf = int(line[i])
        files[total_index] = (i//2, cf)
        if i+1 < len(line) and line[i+1] != "0":
            c = int(line[i+1])
            heappush(spaces[c], total_index+cf)
            total_index += c
        total_index += cf


    print(part1(files, spaces))
    print(part2(files, spaces))


if __name__ == "__main__":
    main()

# year
# solution for 09.01: 6432869891895
# solution for 09.02: 6467290479134
