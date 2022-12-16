import io

from advent.days.day14 import Wall, first, second

data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
data_io = io.StringIO(data)


def test_wall_parse():
    wall = Wall(io.StringIO(data).read().rstrip())
    print()
    print(wall)


def test_first():
    assert first(io.StringIO(data)) == 24


def test_second():
    assert second(io.StringIO(data)) == 93
