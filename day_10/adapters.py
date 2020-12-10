import dataclasses


# FILE = "test.txt"
# FILE = "test2.txt"
FILE = "adapters.txt"


def read():
    data = []

    with open(FILE, "r") as f:
        for line in f:
            line = line.strip()
            data.append(int(line))

    builtin = max(data) + 3
    data.append(builtin)
    data.sort()

    return data


def part1():
    data = read()

    current = 0
    jolt_diff1s = 0
    jolt_diff2s = 0
    jolt_diff3s = 0

    while len(data):
        new = data.pop(0)
        diff = new - current

        if diff == 1:
            jolt_diff1s += 1
        elif diff == 2:
            jolt_diff2s += 1
        elif diff == 3:
            jolt_diff3s += 1
        else:
            raise Exception

        current = new

    print(jolt_diff1s, jolt_diff3s)
    print(jolt_diff1s * jolt_diff3s)


@dataclasses.dataclass
class Data:
    data: list
    current: int = 0

    def clone(self):
        return dataclasses.replace(self, data=self.data[:])

    def freeze(self):
        return (tuple(self.data), self.current)


memos = {}


def count_ways(data_orig):
    if not len(data_orig.data):
        return 1

    frozen = data_orig.freeze()
    cached = memos.get(frozen)
    if cached is not None:
        return cached

    data = data_orig.clone()

    new = data.data.pop(0)
    diff = new - data.current

    total_ways = 0

    while diff <= 3:
        if diff not in (1, 2, 3):
            raise Exception

        data_copy = data.clone()
        data_copy.current = new
        total_ways += count_ways(data_copy)

        try:
            new = data.data.pop(0)  # pop another one
        except IndexError:
            break

        diff = new - data.current

    memos[frozen] = total_ways
    return total_ways


def part2():
    data = Data(read())
    print(count_ways(data))


part1()
# part2()
