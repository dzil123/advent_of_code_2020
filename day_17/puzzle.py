from collections import defaultdict

# part 2, dimensions = 4

# FILE = "test.txt"
FILE = "puzzle.txt"


ACTIVE = "#"
INACTIVE = "."


def read():
    data = defaultdict(lambda: INACTIVE)
    with open(FILE, "r") as f:
        for x, line in enumerate(x for x in f if x.strip()):
            line = line.strip()
            for y, val in enumerate(line):
                data[x, y, 0, 0] = val
    return data


def get_adj(data, pos):
    total = 0

    for x_d in range(-1, 2):
        for y_d in range(-1, 2):
            for z_d in range(-1, 2):
                for w_d in range(-1, 2):
                    if (x_d, y_d, z_d, w_d) == (0, 0, 0, 0):
                        continue

                    new_pos = (pos[0] + x_d, pos[1] + y_d, pos[2] + z_d, pos[3] + w_d)

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
