from collections import Counter

def is_valid1(s):
    return max(Counter(s).values()) >= 2 and list(s) == sorted(s)

def is_valid2(s):
    return 2 in Counter(s).values() and list(s) == sorted(s)

print(sum([is_valid1(str(i)) for i in range(236491, 713787)]))
print(sum([is_valid2(str(i)) for i in range(236491, 713787)]))


