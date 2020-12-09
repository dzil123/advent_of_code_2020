# FILE, PREAMBLE = "test.txt", 5
FILE, PREAMBLE = "puzzle.txt", 25

xmas = []

with open(FILE, "r") as f:
    for line in f:
        line = line.strip()
        xmas.append(int(line))


def is_valid(index, number):
    array = xmas[index : index + PREAMBLE]
    for a in array:
        for b in array:
            if a + b == number:
                return True
    return False


def part1():
    for index, number in enumerate(xmas[PREAMBLE:]):
        if not is_valid(index, number):
            return number

    raise Exception


def part2():
    invalid = part1()

    for start_index in range(len(xmas)):
        for end_index in range(PREAMBLE + 2, len(xmas) + 1):
            array = xmas[start_index:end_index]
            total = sum(array)

            if total == invalid:
                return min(array) + max(array)
            elif total > invalid:
                break

    raise Exception


# print(part1())
print(part2())
