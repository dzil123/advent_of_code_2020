import re
import dataclasses
from pprint import pprint
from collections import deque, defaultdict

FILE = "test.txt"
# FILE = "test2.txt"
# FILE = "puzzle.txt"

# 10x10 image

@dataclasses.dataclass(frozen=True)
class Tile:
    north: tuple[str] # left to right
    south: tuple[str] # left to right
    east: tuple[str] # top to bottom
    west: tuple[str] # top to bottom

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

    def get_side(self, side: int):
        return (self.north, self.south, self.east, self.west)[side]

    def rotate(self):
        north = self.west[::-1]
        south = self.east[::-1]
        east = self.north[:]
        west = self.south[:]

        return self._create(north, south, east, west)
    
    def flip_h(self):
        north = self.north[::-1]
        south = self.south[::-1]
        east = self.west[:]
        west = self.east[:]

        return self._create(north, south, east, west)

    def apply_rule(self, rule):
        if rule == "h":
            return self.flip_h()
        elif rule == "r":
            return self.rotate()
    
    def apply_rules(self, rules):
        tile = self
        for rule in rules:
            tile = tile.apply_rule(rule)
        return tile

    def generate_orientations(self, id):
        ORIENTATIONS = [[], ['h'], ['h', 'r'], ['h', 'r', 'h'], ['h', 'r', 'r'], ['h', 'r', 'r', 'h'], ['h', 'r', 'r', 'r'], ['h', 'r', 'r', 'r', 'h']]
        for orientation in ORIENTATIONS:
            yield OrientedTile(orientation=orientation, orig_tile=self, id=id)

@dataclasses.dataclass(frozen=True)
class OrientedTile:
    orientation: tuple[str]
    orig_tile: Tile
    id: int
    tile: Tile = dataclasses.field(init=False, compare=False)

    def __post_init__(self):
        # self.tile = self.orig_tile.apply_rules(self.orientation)
        object.__setattr__(self, "tile", self.orig_tile.apply_rules(self.orientation))
    
    def __repr__(self):
        return f"Tile({self.id}, {self.orientation})"

@dataclasses.dataclass(frozen=True)
class Side:
    tile: OrientedTile
    side: int # N=0, S=1, E=2, W=3

    def get(self):
        return self.tile.tile.get_side(self.side)

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
    
    return tile_id, Tile.make(tile)

def read():
    tiles = {}

    with open(FILE, "r") as f:
        while (tile := read_tile(f)) is not None:
            tile_id, tile = tile
            tiles[tile_id] = tile
    
    return tiles

def generate_orientations(tile, hist=None, seen=None):
    if hist is None:
        hist = []
    if seen is None:
        seen = set()
        seen.add(tile)
        yield hist

    for op, new_tile in (("r", tile.rotate()), ("h", tile.flip_h()))[::-1]:
        if not new_tile in seen:
            new_hist = hist + [op]
            seen.add(new_tile)
            yield new_hist

            yield from generate_orientations(new_tile, new_hist, seen)

def part1():
    tiles = read()

    # tile_id, tile = tiles.popitem()
    # return list(generate_orientations(tile))

    north_south = defaultdict(list)
    for id, tile in tiles.items():
        for tile in tile.generate_orientations(id):
            for side in (0, 1):
                side = Side(tile=tile, side=side)
                north_south[side.get()].append(side)
    
    pprint(north_south)


# pprint(read().popitem())
print(part1())
