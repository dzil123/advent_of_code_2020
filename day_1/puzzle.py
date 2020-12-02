from itertools import combinations
from math import prod

WANTED_SUM = 2020
NUM_ENTRIES = 2
# NUM_ENTRIES = 3

numbers = []

with open("puzzle.txt", "r") as f:
    for line in f:
        numbers.append(int(line.strip()))

for attempt in combinations(numbers, NUM_ENTRIES):
    if sum(attempt) == WANTED_SUM:
        print(attempt, prod(attempt))
