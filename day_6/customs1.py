# FILE = "test.txt"
FILE = "customs.txt"

groups = []

with open(FILE, "r") as f:
    group = ""
    for line in f:
        line = line.strip()
        if not line:  # newline, end of group
            ans = len(set(group))
            groups.append(ans)
            group = ""
        group += line  # concat all responses within a group to a single string
    ans = len(set(group))  # deduplicate the letters and count the length
    groups.append(ans)
    group = ""

print(sum(groups))
