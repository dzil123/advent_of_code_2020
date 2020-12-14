import itertools

# FILE = "test.txt"
# FILE = "test2.txt"
FILE = "puzzle.txt"

# PART = 1
PART = 2


def read_mask(line):
    masks = []

    raw_mask = line.split()[-1]  # the string of 1, 0, X
    for i, n in enumerate(reversed(raw_mask)):  # reverse so least sig bit is i=0
        i = 2 ** i

        if PART == 1:
            if n == "X":
                continue

            n = bool(int(n))  # 1 = set bit on, 0 = set bit off
            mask = [i, n]

        elif PART == 2:
            if n == "0":
                continue
            elif n == "1":
                mask = [set_high(i)]
            elif n == "X":
                mask = [set_high(i), set_low(i)]

        masks.append(mask)

    if PART == 2:
        masks = list(itertools.product(*masks))

    return masks


def read_mem(line):
    line = line.split()

    address = int(line[0][4:][:-1])  # trim off "mem[" and "]"
    data = int(line[-1])

    return [address, data]


def set_high(i):
    def partial(val):
        return val | i

    return partial


def set_low(i):
    def partial(val):
        return val & ~i

    return partial


def apply_mask_part1(val, masks: list[tuple[int, bool]]):
    for i, n in masks:
        if n:
            val |= i
        else:
            val &= ~i

    return val


def apply_mask_part2(raw_address, masks):
    for mask in masks:  # for each possible combination generated by itertools.product
        address = raw_address
        for m in mask:
            address = m(address)

        yield address


def run():
    memory = {}
    masks = []

    with open(FILE, "r") as f:
        for line in f:
            line = line.strip()

            if line.startswith("mask"):
                masks = read_mask(line)

            elif line.startswith("mem"):
                raw_address, data = read_mem(line)

                if PART == 1:
                    memory[raw_address] = apply_mask_part1(data, masks)

                elif PART == 2:
                    for address in apply_mask_part2(raw_address, masks):
                        memory[address] = data

    return sum(memory.values())


print(run())
