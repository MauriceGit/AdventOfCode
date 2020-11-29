

def is_valid(s, exactly_double):
    double_digit = False
    for i in range(1, 6):
        if s[i-1] == s[i] and (not exactly_double or ((i<=1 or s[i-2] != s[i]) and (i>=5 or s[i+1] != s[i]))):
            double_digit = True
        if int(s[i-1]) > int(s[i]):
            return 0

    return 1 if double_digit else 0


number_range = [236491, 713787]
keys = 0
for i in range(number_range[0], number_range[1]):
    # False for the first puzzle
    # True for the second puzzle
    keys += is_valid(str(i), False)

print(keys)


# solution for 04.01: 1169
# solution for 04.02: 757
