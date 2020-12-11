import itertools
from pprint import pprint

# FILE = "test.txt"
FILE = "puzzle.txt"

# PART = 1
PART = 2

# DEBUG = True
DEBUG = False

if PART == 1:
    MIN_TOTAL = 4
elif PART == 2:
    MIN_TOTAL = 5


def read():
    data = []
    with open(FILE, "r") as f:
        for line in f:
            line = line.strip()
            data.append(list(line))
    return data


def show(data):
    if not DEBUG:
        return
    data = ["".join(str(item) for item in row) for row in data]
    pprint(data)


def pause():
    if DEBUG:
        input()


def get_adj(data, row, col):
    occupied = data[row][col] == "#"
    total = 0

    for row_d in [-1, 0, 1]:
        for col_d in [-1, 0, 1]:
            if row_d == 0 and col_d == 0:
                continue

            try:
                if PART == 1:
                    new_row = row + row_d
                    new_col = col + col_d

                    if new_row < 0 or new_col < 0:
                        continue

                    seat = data[new_row][new_col]

                    if seat == "#":
                        total += 1

                elif PART == 2:
                    for i in itertools.count(1):
                        new_row = row + (row_d * i)
                        new_col = col + (col_d * i)

                        if new_row < 0 or new_col < 0:
                            raise IndexError

                        seat = data[new_row][new_col]

                        if seat == "#":
                            total += 1
                        if seat == "#" or seat == "L":
                            break

            except IndexError:
                continue

    return occupied, total


def get_sitting(data):
    total = 0

    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == "#":
                total += 1

    return total


def run(data):
    while True:
        new_data = [col[:] for col in data]
        sitting = [col[:] for col in data]

        for row in range(len(data)):
            for col in range(len(data[row])):
                if data[row][col] == ".":
                    continue

                occupied, total = get_adj(data, row, col)
                sitting[row][col] = total

                if not occupied:
                    if total == 0:
                        occupied = True
                else:
                    if total >= MIN_TOTAL:
                        occupied = False

                new_data[row][col] = "#" if occupied else "L"

        if new_data == data:
            break

        show(data)
        show(sitting)
        pause()

        data = new_data

    return data


def main():
    data = read()
    data = run(data)

    total = get_sitting(data)
    print(total)


main()
