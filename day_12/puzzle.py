import math

FILE = "test.txt"
FILE = "puzzle.txt"

data = []

with open(FILE, "r") as f:
    for line in f:
        line = line.strip()
        action, param = line[0], line[1:]
        data.append((action, int(param)))

pos = [0, 0]
angle = 0  # angle 0 = (1, 0), positive angle is counterclockwise

for action, param in data:
    if action == "N":
        pos[1] += param
    elif action == "S":
        pos[1] -= param
    elif action == "E":
        pos[0] += param
    elif action == "W":
        pos[0] -= param
    elif action == "L":
        angle += param
    elif action == "R":
        angle -= param
    elif action == "F":
        rad = math.radians(angle)
        pos[0] += math.cos(rad) * param
        pos[1] += math.sin(rad) * param

distance = math.hypot(*pos)
manhat_dist = sum(abs(x) for x in pos)

print(pos, angle, distance, manhat_dist)
