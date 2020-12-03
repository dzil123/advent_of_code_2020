grid = []

with open("trees.txt", "r") as f:
    for line in f:
        grid.append(line.strip())

# SLOPES = [[3, 1]]  # problem 1
SLOPES = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]  # problem 2
mul_trees = 1

for slope in SLOPES:
    trees = 0
    for i, y in enumerate(range(0, len(grid), slope[1])):
        x = i * slope[0]
        print(x, y)
        square = grid[y][x % len(grid[y])]
        if square == "#":
            trees += 1
    print(trees)
    mul_trees *= trees

print(mul_trees)
