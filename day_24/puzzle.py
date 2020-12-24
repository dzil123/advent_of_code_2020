import enum
from collections import defaultdict
from pprint import pprint

FILE = "test.txt"
FILE = "puzzle.txt"


class Dir(enum.Enum):
    NE = (1, -1)
    NW = (0, -1)
    SE = (0, 1)
    SW = (-1, 1)
    E = (1, 0)
    W = (-1, 0)


def parse_line(line):
    line = line.strip()
    data = []

    while line:
        for dir in Dir:
            dir_n = dir.name.lower()
            if line.startswith(dir_n):
                line = line[len(dir_n) :]
                data.append(dir)
                break
        else:
            raise ValueError(line)

    return data


def read():
    with open(FILE, "r") as f:
        return [parse_line(line) for line in f]


def bounds(tiles):
    low = (min(tile[0] for tile in tiles), min(tile[1] for tile in tiles))
    high = (max(tile[0] for tile in tiles), max(tile[1] for tile in tiles))
    return (low, high)


def add(tile, dir):
    inst = dir.value
    return (tile[0] + inst[0], tile[1] + inst[1])


def num_neighbors(tiles, tile):
    return sum(tiles[add(tile, dir)] for dir in Dir)


def enumerate_tiles(limits):
    for x in range(limits[0][0], limits[1][0] + 1):
        for y in range(limits[0][0], limits[1][0] + 1):
            yield (x, y)


def part1():
    data = read()
    tiles = defaultdict(lambda: False)

    for line in data:
        tile = (0, 0)
        for dir in line:
            tile = add(tile, dir)
        tiles[tile] = not tiles[tile]

    print(sum(tiles.values()))
    return tiles


def part2(tiles):
    MOVES = 100
    # MOVES = 10
    AREA = int(MOVES * 1.1)
    limits = bounds(tiles)

    print(limits)
    limits = (
        (limits[0][0] - AREA, limits[0][1] - AREA),
        (limits[1][0] + AREA, limits[1][1] + AREA),
    )
    print(limits)

    for tile in enumerate_tiles(limits):
        tiles[tile]  # generate default white tile

    print(f"Day 0: {sum(tiles.values())}")
    for day in range(1, MOVES + 1):
        new_tiles = tiles.copy()
        for tile in enumerate_tiles(limits):
            adj = num_neighbors(tiles, tile)

            tile_val = tiles[tile]
            if tile_val:  # black
                if adj == 0 or adj > 2:
                    tile_val = False
            else:  # white
                if adj == 2:
                    tile_val = True

            new_tiles[tile] = tile_val
        tiles = new_tiles

        # print(f"Day {day}: {sum(tiles.values())}")
    print(f"Day {day}: {sum(tiles.values())}")


def run():
    tiles = part1()
    part2(tiles)


run()
