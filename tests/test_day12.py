import io

from advent.days.day12 import first, second

data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
data_io = io.StringIO(data)


def test_first():
    assert first(io.StringIO(data)) == 31


def test_second():
    assert second(io.StringIO(data)) == 29
