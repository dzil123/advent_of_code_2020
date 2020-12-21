import re
import dataclasses
from pprint import pprint
from collections import deque, defaultdict, Counter
import random

FILE = "test.txt"
# FILE = "test2.txt"
# FILE = "puzzle.txt"

# only the sides
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
            yield OrientedTile(orientation=tuple(orientation), orig_tile=self, id=id)

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
        # row = [char == "#" for char in line if char in ".#"]
        row = line
        tile.append(row)
    
    return tile_id, tile, Tile.make(tile)

def read():
    tiles = {}
    raw_tiles = {}

    with open(FILE, "r") as f:
        while (tile := read_tile(f)) is not None:
            tile_id, raw_tile, tile = tile
            tiles[tile_id] = tile
            raw_tiles[tile_id] = raw_tile
    
    return raw_tiles, tiles

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

def same_tiles(tiles, sides):
    variable = defaultdict(lambda: defaultdict(list))
    for id, tile in tiles.items():
        for tile in tile.generate_orientations(id):
            for side in sides:
                side = Side(tile=tile, side=side)
                variable[side.get()][side.tile.id].append(side)
    
    return variable

def part1(data):
    _, tiles = data

    n_s = same_tiles(tiles, (0, 1))
    e_w = same_tiles(tiles, (2, 3))

    # pprint(n_s)
    # print()
    # pprint(e_w)

    for d in (n_s, e_w): # why do both give the same answer?
        counter = Counter()
        for v in d.values():
            if len(v) == 1: # if on the edge
                counter.update(v.keys())
        print(counter.most_common())
        total = 1
        for x, n in counter.most_common():
            if n == 4: # not sure why 4, when exists n=2
                # maybe because 8 valid rotations of the unique solution, then halved because only one direction
                print(x, end=" ")
                total *= x
        print()
        print(total)
        print()

def adjacency(n_s, e_w):
    # tiles = defaultdict(lambda: defaultdict) # dict[tile_id, dict[orientation, dict[side_int, Side]]]
    # tiles = defaultdict(lambda: {}) # dict[tile_id, dict[Side, Side-other]]
    tiles = defaultdict(lambda: {}) # dict[tile_id, dict[Side, Side-other]]

    for d in (n_s, e_w):
        for touching in d.values():
            if len(touching) != 2:
                continue
            touching = list(touching.items())
            # print(touching)
            for this, other in ((touching[0], touching[1]), (touching[1], touching[0])):
                this_id, this_sides = this
                other_sides = other[1]

                # print(this_id, this_sides, other_sides)

                for this_side in this_sides:
                    for other_side in other_sides:
                        if this_side.side != other_side.side:
                            # print(" ", this_id, this_side, other_side)
                            tiles[this_id][this_side] = other_side

    # for key, value in tiles.items():
    #     tiles[key] = dict(sorted(value.items()))

    return tiles

def assemble_tiles(tiles):
    n_s = same_tiles(tiles, (0, 1))
    e_w = same_tiles(tiles, (2, 3))

    adjacent = adjacency(n_s, e_w)

    random_tile_id = random.choice(list(adjacent.keys())) # pick random tile to be at the center
    random_tile_orientation = random.choice(list(adjacent[random_tile_id].keys())).tile # and random orientation

    image = {} # 2d array but sparse, dict[position(row(int), column(int)), OrientedTile]
    current_pos = (0, 0)
    image[current_pos] = random_tile_orientation

    queue = deque((current_pos,))
    seen = set()
    SIDE_DIRECTION = ((-1, 0), (1, 0), (0, 1), (0, -1)) # NSEW, (y, x) (row, column)

    while queue:
        current_pos = queue.pop()
        current_tile = image[current_pos]
        next_tiles = {side.side: touching for side, touching in adjacent[current_tile.id].items() if side.tile == current_tile}
        print(next_tiles)

        for side, touching_side in next_tiles.items():
            direction = SIDE_DIRECTION[side]
            next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
            touching = touching_side.tile

            assert (expected := image.get(next_pos)) is None or expected == touching
            
            image[next_pos] = touching
            if next_pos not in seen:
                seen.add(next_pos)
                queue.append(next_pos)
    
    return image

def get_bounds(positions):
    low = [0, 0]
    high = [0, 0]

    for x, y in positions:
        if x < low[0]:
            low[0] = x
        if x > high[0]:
            high[0] = x
        
        if y < low[1]:
            low[1] = y
        if y > high[1]:
            high[1] = y
    
    extents = [high[0] - low[0] + 1, high[1] - low[1] + 1]
    print(low, high, extents)
    return low, high, extents

def trim_tile(tile):
    return [row[1:-1] for row in tile[1:-1]]

def rotate_full_tile(tile, orientation):
    for rule in orientation:
        if rule == "h":
            tile = [row[::-1] for row in tile]
        elif rule == "r":
            tile = list(zip(*reversed(tile)))
    return tile

def part2(data):
    raw_tiles, tiles = data
    size = (8, 8) # 10x10 tiles, trimmed on each edge
    # pprint(raw_tiles)

    image = assemble_tiles(tiles)
    low, high, extents = get_bounds(list(image.keys()))
    # pprint(image)
    print()

    trimmed_raw_tiles = {id: trim_tile(tile) for id, tile in raw_tiles.items()}
    filled_image = {pos: rotate_full_tile(trimmed_raw_tiles[tile.id], tile.orientation) for pos, tile in image.items()}

    final_image = [[filled_image[low[0]+row//size[0], low[1]+col//size[1]][row%size[0]][col%size[1]] for col in range(size[1] * extents[1]) ] for row in range(size[0] * extents[0])]
    final_image = [''.join(row) for row in final_image]
    print('\n'.join(final_image))


def run():
    data = read()
    part1(data)
    part2(data)

run()
