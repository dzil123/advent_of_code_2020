from math import ceil
import math

# FILE = "test.txt"
FILE = "puzzle.txt"

buses = []
ordered_buses = []

with open(FILE, "r") as f:
    start = int(f.readline().strip())

    for bus in f.readline().strip().split(","):
        if bus == "x":
            ordered_buses.append(None)
            continue
        bus = int(bus)

        buses.append(bus)
        ordered_buses.append(bus)


def wait_time(bus):
    return -(start % -bus)


def part1():
    earliest = min(buses, key=wait_time)

    return earliest * wait_time(earliest)


# convert the sparse list ordered_buses into a dict {index/delay: bus}
def sparse():
    return {delay: bus for delay, bus in enumerate(ordered_buses) if bus is not None}


# the input is given as (delay, bus), where `(x + delay) % bus == 0`
# this converts from the input data to (divisor, remainder), where `x % divisor == remainder`
# sorted by divisor greatest to least [(divisor, remainder)...] as an optimization
def get_mods():
    mods = ((bus, (bus - delay) % bus) for delay, bus in sparse().items())
    mods = sorted(mods, reverse=True)

    return mods


# "systematic search" - too slow for real input
def part2():
    import itertools

    for time in itertools.count(buses[0], buses[0]):
        for delay, bus in sparse().items():
            if (time + delay) % bus != 0:
                break
        else:
            return time


# https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Search_by_sieving
def part2reloaded():
    x = 0
    step = 1

    for divisor, remainder in get_mods():
        while x % divisor != remainder:
            x += step

        step *= divisor

    return x


# print(part1())
# print(part2())
print(part2reloaded())
