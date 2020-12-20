import re
import dataclasses
from pprint import pprint
from collections import deque

FILE = "test.txt"
# FILE = "test2.txt"
# FILE = "puzzle.txt"

# 10x10 image

@dataclasses.dataclass(frozen=True)
class Sides:
    north: tuple[str]
    south: tuple[str]
    east: tuple[str]
    west: tuple[str]

    @classmethod
    def _create(cls, north, south, east, west):
        return cls(north=tuple(north), south=tuple(south), east=tuple(east), west=tuple(west))

    @classmethod
    def make(cls, tile):
        north = tile[0]
        south = tile[-1]
        east = [row[-1] for row in tile]
        west = [row[0] for row in tile]

        return cls._create(north, south, east, west)

    def rotate(self):
        north = self.west[::-1]
        south = self.east[::-1]
        east = self.north[:]
        west = self.south[:]

        return self._create(north, south, east, west)
    
    def rotate_ccw(self):
        north = self.east[:]
        south = self.west[:]
        east = self.south[::-1]
        west = self.north[::-1]

        return self._create(north, south, east, west)

    def flip_h(self):
        north = self.north[::-1]
        south = self.south[::-1]
        east = self.west[:]
        west = self.east[:]

        return self._create(north, south, east, west)

    def flip_v(self):
        north = self.south[:]
        south = self.north[:]
        east = self.east[::-1]
        west = self.west[::-1]

        return self._create(north, south, east, west)
        # return cls(north=north, south=south, east=east, west=west)


def read_tile(f):
    R = r"Tile (\d+)\:"
    match = re.match(R, f.readline().strip())
    if match is None:
        return None
    tile_id = int(match[1])

    tile = []
    while (line := f.readline().strip()):
        row = [char == "#" for char in line if char in ".#"]
        tile.append(row)
    
    return tile_id, Sides.make(tile)

def read():
    tiles = {}

    with open(FILE, "r") as f:
        while (tile := read_tile(f)) is not None:
            tile_id, tile = tile
            tiles[tile_id] = tile
    
    return tiles

def generate_orientations(tile):
    seen = set()
    queue = deque([tile])

    while queue:
        tile = queue.pop()
        
        # for new_tile in (tile.rotate(), tile.rotate_ccw(), tile.flip_h(), tile.flip_v()):
        for new_tile in (tile.rotate(), tile.flip_h()):
            if not new_tile in seen:
                seen.add(new_tile)
                queue.append(new_tile)
    
    return list(seen)

def part1():
    tiles = read()


# pprint(read().popitem())
print(part1())
