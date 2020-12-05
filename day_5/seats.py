# FILE = "test.txt"
FILE = "seats.txt"

ids = []

with open(FILE, "r") as f:
    for line in f:
        line = line.strip()
        low, high = 0, 127
        for char in line[:7]:
            if char == "F":
                high = (low + high) // 2
            elif char == "B":
                low = (low + high) // 2 + 1
            else:
                raise Exception("char", line, char, low, high)
            # print(low, high)
            if low == high:
                break
        # print("row", low, high)
        assert low == high
        row = low

        low, high = 0, 7
        for char in line[7:]:
            if char == "L":
                high = (low + high) // 2
            elif char == "R":
                low = (low + high) // 2 + 1
            else:
                raise Exception("char", line, char, low, high)
            # print(low, high)
            if low == high:
                break
        # print("col", low, high)
        assert low == high
        col = low

        id = row * 8 + col
        # print(row, col, id)
        ids.append(id)

print(max(ids))  # part 1

# part 2
ids.sort()
# print(ids[0], ids[-1])
all_seats = range(ids[0], ids[-1] + 1)
ids = set(all_seats).difference(ids)
print(ids)
