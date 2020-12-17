from collections import defaultdict
import itertools

# FILE = "test.txt"
FILE = "puzzle.txt"

DIMS = 4  # dimensions: 3 or 4

ACTIVE = "#"
INACTIVE = "."


def read():
    data = defaultdict(lambda: INACTIVE)
    with open(FILE, "r") as f:
        for x, line in enumerate(x for x in f if x.strip()):
            line = line.strip()
            for y, val in enumerate(line):
                pos = [0] * DIMS
                pos[0:2] = x, y
                pos = tuple(pos)

                data[pos] = val
    return data


def get_adj(data, pos):
    total = 0

    for deltas in itertools.product(range(-1, 2), repeat=DIMS):
        if deltas == (0,) * DIMS:
            continue

        new_pos = tuple(sum(x) for x in zip(pos, deltas))

        # this access will generate an inactive if it doesnt exist yet, due to defaultdict
        # in this way we dont have
        if data[new_pos] == ACTIVE:
            total += 1

    return data[pos], total


def get_active(data):
    total = 0

    for val in data.values():
        if val == ACTIVE:
            total += 1

    return total


def run(data):
    for _ in range(6):
        for pos in list(data.keys()):
            get_adj(data, pos)  # generate inactives next to each pos

        new_data = data.copy()

        for pos in list(data.keys()):
            active, total = get_adj(data, pos)

            if active == ACTIVE:
                if total not in (2, 3):
                    active = INACTIVE
            else:
                if total == 3:
                    active = ACTIVE

            new_data[pos] = active

        data = new_data

    return data


def main():
    data = read()
    data = run(data)

    total = get_active(data)
    print(total)


main()
