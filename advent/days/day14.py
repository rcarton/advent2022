import itertools as it
from typing import Dict, TextIO

from advent.matrix import Coord


class Wall:
    min_row: int | None = None
    max_row: int | None = None
    min_col: int | None = None
    max_col: int | None = None

    infinite_floor: bool
    sand_source: Coord
    data: Dict[Coord, str]

    def __getitem__(self, c: Coord) -> str | None:
        val = self.data.get(c)
        if self.infinite_floor and val is None and c[0] == self.max_row:
            self[c] = '#'
            return '#'
        return val

    def __setitem__(self, c: Coord, value: str) -> None:
        row, col = c
        if self.max_row is None or row > self.max_row:
            self.max_row = row
        if self.min_row is None or row < self.min_row:
            self.min_row = row
        if self.max_col is None or col > self.max_col:
            self.max_col = col
        if self.min_col is None or col < self.min_col:
            self.min_col = col
        self.data[c] = value

    def __init__(self, data: str, infinite_floor: bool = False):
        self.the_void = True
        self.data = {}
        self.infinite_floor = infinite_floor
        segments = []
        for row in data.splitlines():
            segment = []
            for coord_s in row.split(' -> '):
                col, row = [int(n) for n in coord_s.split(',')]
                segment.append((int(row), int(col)))
            segments.append(segment)

        # Populate the segments now
        for segment in segments:
            for (r1, c1), (r2, c2) in it.pairwise(segment):
                r_step = 1 if r2 >= r1 else -1
                c_step = 1 if c2 >= c1 else -1
                for r in range(r1, r2 + r_step, r_step):
                    for c in range(c1, c2 + c_step, c_step):
                        self[r, c] = '#'

        if self.infinite_floor:
            self.max_row += 2

        # Sand starting point
        self.sand_source = (0, 500)
        self[self.sand_source] = '+'

    def __str__(self):
        out = ''
        for row in range(0, self.max_row + 1):
            # out += f'{str(row).rjust(3, " ")} '
            for col in range(self.min_col, self.max_col + 1):
                val = self[row, col]
                out += str(val if val is not None else '.')
            out += '\n'
        return out[:-1]


def add_sand(wall: Wall) -> Coord | None:
    sr, sc = wall.sand_source

    while True:
        if not wall.infinite_floor and sr + 1 > wall.max_row:
            # The Void
            return None

        if wall[sr, sc] == 'o':
            # Full
            return None

        if wall[sr + 1, sc] is None:
            sr += 1
            continue

        # Block below is blocked, attempt falling to the left
        fall_left = (sr + 1, sc - 1)
        if not wall.infinite_floor and fall_left[1] < wall.min_col:
            return None

        if wall[fall_left] is None:
            sr, sc = fall_left
            continue

        # Left is blocked, attempt falling to the right
        fall_right = (sr + 1, sc + 1)
        if not wall.infinite_floor and fall_right[1] > wall.max_col:
            return None

        if wall[fall_right] is None:
            sr, sc = fall_right
            continue

        # Right is blocked, rest here
        wall[sr, sc] = 'o'
        return sr, sc


def first(input: TextIO) -> int:
    wall = Wall(input.read().rstrip())
    count = 0
    while add_sand(wall):
        count += 1
    print()
    print(wall)
    return count


def second(input: TextIO) -> int:
    wall = Wall(input.read().rstrip(), infinite_floor=True)

    count = 0
    while add_sand(wall):
        count += 1
    print()
    print(wall)
    return count
