import itertools as it
from collections import deque
from dataclasses import dataclass
from typing import Iterable, Iterator, List, Literal, TextIO, Tuple, TypeVar

from advent.utils import binseq_to_int

ROCKS_S = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""

STARTING_LEFT_OFFSET = 2
STARTING_VERT_OFFSET = 2
CHAMBER_WIDTH = 7
FULL_LINE = (1 << 7) - 1  # 127
# 64: LIMIT_LEFT = 1 << (CHAMBER_WIDTH - 1)
SHAPES = [[binseq_to_int(line.rstrip()
                         .ljust(7, '.')
                         .replace('#', '1')
                         .replace('.', '0')) >> 2 for line in r.split('\n')]
          for r in ROCKS_S.split('\n\n')]

Move = Literal['<'] | Literal['>'] | Literal['v']


@dataclass
class Rock:
    val: List[int]
    # Height is relative compared to the top of the chamber, 0 means the bottom row of the rock overlaps the highest row
    # of the chamber
    height: int = 4


Chamber = List[int]
DEFAULT_CHAMBER = [(1 << CHAMBER_WIDTH) - 1]  # All 1s on the first row

DEFAULT_ROW = (1 << (CHAMBER_WIDTH + 1)) | 1  # 257: 100000001


def get_chamber_row_with_walls(c: Chamber, h: int) -> int:
    """
    Walls are used to check for moves with &:
          |.###...|
     ->   101110001
    """
    return (get_chamber_row(c, h) << 1) | DEFAULT_ROW


def get_chamber_row(c: Chamber, h: int) -> int:
    """
          .###...
     ->   0111000
    """
    # h == 0 means the top row of the chamber (== c[-1]
    if h > 0:
        return 0
    return c[h - 1]


def can_move(r: Rock, c: Chamber, m: Move) -> bool:
    if m == '<':
        return all(
            get_chamber_row_with_walls(c, r.height + h) & (row << 2) == 0 for h, row in enumerate(reversed(r.val)))
    if m == '>':
        return all(
            get_chamber_row_with_walls(c, r.height + h) & row == 0 for h, row in enumerate(reversed(r.val)))
    if m == 'v':
        return all(
            get_chamber_row_with_walls(c, r.height + h - 1) & (row << 1) == 0 for h, row in enumerate(reversed(r.val)))

    raise Exception('🐞')


def move(r: Rock, c: Chamber, m: Move) -> bool:
    if m == 'v' and r.height > 1:
        r.height -= 1
        return True

    if can_move(r, c, m):
        if m == '<':
            r.val = [row << 1 for row in r.val]
        elif m == '>':
            r.val = [row >> 1 for row in r.val]
        else:
            r.height -= 1
        return True

    if m == 'v':
        # We have to update the chamber before returning False
        for h, row in enumerate(reversed(r.val)):
            if r.height + h > 0:
                # We append the row
                c.append(row)
            else:
                # Merge the rows
                c[r.height + h - 1] = get_chamber_row(c, r.height + h) | row
    return False


def repr_row(row: int, char='#'):
    return bin(row)[2:].replace('1', char).replace('0', '.').rjust(CHAMBER_WIDTH, '.')


def repr_chamber(c: Chamber, r: Rock | None) -> str:
    if r is not None:
        chamber_rows = c[1:] + [0] * (r.height - 1) + [0] * len(r.val)
        rock_rows = [0] * (len(c) - 1) + [0] * (r.height - 1) + r.val[::-1]
        shift = r.height
        while shift <= 0 and len(chamber_rows) > 1:
            shift += 1
            rock_rows.pop(0)
    else:
        chamber_rows = c[1:]
        rock_rows = [0] * len(chamber_rows)

    o = ['+-------+\n']
    for cr, rr in zip(chamber_rows, rock_rows):
        if cr and rr:
            cr_s = repr_row(cr)
            rr_s = repr_row(rr, '@')
            o_s = ''.join('#' if aa == '#' else '@' if bb == '@' else '.' for aa, bb in zip(cr_s, rr_s))
            o += [f'|{o_s}|\n']
        elif cr:
            o += [f'|{repr_row(cr)}|\n']
        else:
            o += [f'|{repr_row(rr, "@")}|\n']
    o = list(reversed(o))
    return ''.join(o)


def compress(c: Chamber) -> int:
    l = len(c)
    for i in range(l):
        r1, r2 = c[l - i - 1], c[l - i - 2]
        if r1 | r2 == FULL_LINE:
            # We can compress, everything before this row can be discarded
            return l - i - 2


CACHE = {}


def cache(i_jets: int, i_shape: int, c: Chamber):
    h = hash((i_jets, i_shape, tuple(c)))
    if h in CACHE:
        raise Exception(f'FOUNNNNND: {(i_jets, i_shape, tuple(c))}')

def try_period(c: Chamber):
    for i in range(len(c) // 100, len(c) // 10):
        if i % 100_000 == 0:
            print(f'Still looking i={i}')
        if c[:i] == c[i:2*i]:
            raise Exception(f'Found period? i={i} len(c)={len(c)}')



def first(input: TextIO, max_rock=2023) -> int:
    c = DEFAULT_CHAMBER
    shapes = it.cycle(enumerate(SHAPES))
    jets = it.cycle(enumerate(input.read().rstrip()))

    i_shape, shape = next(shapes)
    r = Rock(shape)
    i_jets, m = next(jets)
    rock_count = 1

    compressed = 0
    while rock_count < max_rock:

        moved = move(r, c, m)

        if not moved and m == 'v':
            i_shape, shape = next(shapes)
            r = Rock(shape)
            rock_count += 1
            # Try to compress the tower
            # compression = compress(c)
            # if compression:
            #     c = c[compression:]
            #     compressed += compression
            #
            # cache(i_jets, i_shape, c)

            if rock_count % 1_000_000 == 0:
                print(f'rock_count={rock_count}, height={len(c) - 1 + compressed}')
                print(repr_chamber(c, r))

                print("Looking for period..")
                try_period(c)
                print("not found")

        if m == 'v':
            i_jets, m = next(jets)
        else:
            m = 'v'

    return len(c) - 1 + compressed


def second(input: TextIO) -> int:
    return first(input, 1_000_000_000_000)
