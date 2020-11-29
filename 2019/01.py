
# Second part of the challenge
def get_fuel_02(mass):
    new_mass = int(mass)//3 - 2
    if new_mass <= 0:
        return 0
    return new_mass + get_fuel_02(new_mass)

# First part of the challenge
def get_fuel_01(mass):
    return int(mass)//3 - 2

with open("01.data", "r") as f:

    # iterative/explicit style
    #sums = 0
    #for x in f.read().splitlines():
    #    sums += get_fuel_01(x)
    #print(sums)

    # functional style
    print(sum(map(get_fuel_01, f.read().splitlines())))

# solution for 01.01: 3429947
# solution for 01.02: 5142043



