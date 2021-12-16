#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


# returns (version, type_id, number), read_bit_length
def parse_packet(bits, i):

    version = int(bits[i:i+3], 2)
    type_id = int(bits[i+3:i+6], 2)
    i += 6
    # literal value
    value = ""
    if type_id == 4:
        while True:
            next_four = bits[i:i+5]
            i += 5
            value += next_four[1:]
            if next_four[0] == "0":
                break
        return (version, type_id, int(value, 2)), i

    length_type_id = int(bits[i], 2)
    i += 1
    tmp = 15 if length_type_id == 0 else 11
    number = int(bits[i:i+tmp], 2)
    i += tmp

    packets = []
    if length_type_id == 0:
        # number of bits
        tmp_i = i
        while True:
            packet, tmp_i = parse_packet(bits, tmp_i)
            packets.append(packet)
            if tmp_i-i >= number:
                break
        i = tmp_i
    else:
        # number of packets
        for j in range(number):
            packet, i = parse_packet(bits, i)
            packets.append(packet)

    return (version, type_id, packets), i


def parse(bits):
    i = 0
    packets = []
    while True:
        if i >= len(bits) or int(bits[i:], 2) == 0:
            break
        packet, i = parse_packet(bits, i)
        packets.append(packet)

    return packets


def evaluate(p):

    if p[1] == 4:
        return p[2]

    sub_packets = [evaluate(tmp_p) for tmp_p in p[2]]

    if p[1] == 0:
        return sum(sub_packets)
    elif p[1] == 1:
        return reduce(mul, sub_packets)
    elif p[1] == 2:
        return min(sub_packets)
    elif p[1] == 3:
        return max(sub_packets)
    elif p[1] == 5:
        return int(sub_packets[0] > sub_packets[1])
    elif p[1] == 6:
        return int(sub_packets[0] < sub_packets[1])
    elif p[1] == 7:
        return int(sub_packets[0] == sub_packets[1])

    return 0


def version_sum(packets):
    if type(packets) == int:
        return 0
    return sum(p[0] + version_sum(p[2]) for p in packets)


def main():

    lines = open_data("16.data")

    bits = "".join(format(int(c, 16), "04b") for c in lines[0])
    packets = parse(bits)

    print(version_sum(packets))
    print(evaluate(packets[0]))


if __name__ == "__main__":
    main()

# year 2021
# solution for 16.01: 938
# solution for 16.02: 1495959086337
