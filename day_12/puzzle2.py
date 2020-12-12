import math

FILE = "test.txt"
FILE = "puzzle.txt"

data = []

with open(FILE, "r") as f:
    for line in f:
        line = line.strip()
        action, param = line[0], line[1:]
        data.append((action, int(param)))

waypoint = [10, 1]
pos = [0, 0]
# angle 0 = (1, 0), positive angle is counterclockwise


def rotate(waypoint, delta_angle):
    distance = math.hypot(*waypoint)
    angle = math.atan2(waypoint[1], waypoint[0])

    angle += math.radians(delta_angle)
    waypoint[0] = math.cos(angle) * distance
    waypoint[1] = math.sin(angle) * distance

    return waypoint


for action, param in data:
    if action == "N":
        waypoint[1] += param
    elif action == "S":
        waypoint[1] -= param
    elif action == "E":
        waypoint[0] += param
    elif action == "W":
        waypoint[0] -= param
    elif action == "L":
        waypoint = rotate(waypoint, param)
    elif action == "R":
        waypoint = rotate(waypoint, -1 * param)
    elif action == "F":
        pos[0] += waypoint[0] * param
        pos[1] += waypoint[1] * param

distance = math.hypot(*pos)
manhat_dist = sum(abs(x) for x in pos)

print(pos, distance, manhat_dist)
