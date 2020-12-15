from collections import defaultdict, deque

# FILE = "test.txt"
FILE = "puzzle.txt"

# STOP = 2020
STOP = 30000000

with open(FILE, "r") as f:
    line = f.readline().strip()
    data = [int(x) for x in line.split(",")]

history = defaultdict(lambda: deque(maxlen=2))
for i, x in enumerate(data):
    history[x].append(i)

wanted = data[-1]

for i in range(len(data), STOP):
    num = None
    hist = history[wanted]

    if len(hist) == 1:
        num = 0
    else:
        num = hist[-1] - hist[-2]

    wanted = num
    history[num].append(i)

    if i % 200000 == 0:
        print(f"{i / STOP * 100:5.2f}%")

print()
print(num)
