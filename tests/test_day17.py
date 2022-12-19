import io
from typing import Optional, Tuple

import pytest

from advent.days.day17 import CHAMBER_WIDTH, Chamber, Rock, can_move, compress, first, move, repr_chamber, second
from advent.utils import binseq_to_int

data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""
data_io = io.StringIO(data)

data_chamber = """
|.....@.|
|.....@.|
|...@@@.|
|..#....|
|.###...|
|..#....|
|..####.|
+-------+
"""

data_chamber_w_merge = """
|.....@.|
|.....@.|
|..#@@@.|
|.###...|
|..#....|
|..####.|
+-------+
"""

def parse_case(i: str) -> Tuple[Chamber, Optional[Rock]]:
    lines = i.lstrip().rstrip().splitlines()
    lines = [l[1:-1] for l in lines[:-1]]
    rock = []
    rock_height = 1
    c = []
    for line in lines:
        line = line.replace('.', '0')
        rock_line = binseq_to_int(line.replace('@', '1').replace('#', '0'))
        c_line = binseq_to_int(line.replace('@', '0').replace('#', '1'))
        if rock_line:
            rock.append(rock_line)
        if c_line:
            c.insert(0, c_line)
        if not rock_line and not c_line:
            rock_height += 1
        if rock_line and c_line:
            rock_height -= 1
    c.insert(0, (1 << CHAMBER_WIDTH) - 1)
    return c, Rock(rock, rock_height)


def test_parse_case():
    assert repr_chamber(*parse_case(data_chamber)) == data_chamber.lstrip()
    assert repr_chamber(*parse_case(data_chamber_w_merge)) == data_chamber_w_merge.lstrip()

def test_merge():
    r = Rock([2, 2, 14], height=0)
    c = [30, 16, 56, 16]
    print(repr_chamber(c, r))

    assert can_move(r, c, 'v') is False

    assert move(r, c, 'v') is False
    assert r.height == 0
    assert(repr_chamber(c, None).strip()) == """
|.....#.|
|.....#.|
|..####.|
|.###...|
|..#....|
+-------+
""".strip()


def test_move_bottom():
    c, r = parse_case("""
|...@@@@|
+-------+""")
    move(r, c, '<')
    assert(repr_chamber(c, r).strip()) == """
|..@@@@.|
+-------+
""".strip()

    assert can_move(r, c, 'v') is False
    move(r, c, 'v')
    assert(repr_chamber(c, None).strip()) == """
|..####.|
+-------+
""".strip()


def test_compress():
    s = """
|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|..#....|
|.###...|
|..#....|
|.####..|
|######.|
|....###|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+
"""
    c, r = parse_case(s)
    result = compress(c)
    assert result == 8
    c = c[result:]
    assert compress(c) == 0
    print(repr_chamber(c, None))

def test_first():
    assert first(io.StringIO(data)) == 3068


def test_second():
    assert second(io.StringIO(data)) == 1514285714288
