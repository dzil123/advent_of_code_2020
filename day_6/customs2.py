import string

# FILE = "test.txt"
FILE = "customs.txt"

groups = []

with open(FILE, "r") as f:
    group = set(string.ascii_lowercase)  # set of chars, start with every possible item
    for line in f:
        line = line.strip()
        if not line:  # newline, end of group
            ans = len(group)
            groups.append(ans)
            group = set(string.ascii_lowercase)
            continue
        group.intersection_update(line)  # remove items in group that arent in line
    ans = len(group)
    groups.append(ans)
    group = set(string.ascii_lowercase)

print(sum(groups))
