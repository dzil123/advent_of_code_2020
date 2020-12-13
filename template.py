FILE = "test.txt"
# FILE = "test2.txt"
# FILE = "puzzle.txt"


with open(FILE, "r") as f:
    text = [group.split("\n") for group in f.read().split("\n\n")]




data = []

with open(FILE, "r") as f:
    for line in f:
        line = line.strip()
