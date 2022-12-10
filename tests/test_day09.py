import io

from advent.days.day09 import first, second

data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
data_io = io.StringIO(data)

data2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""


def test_first():
    assert first(io.StringIO(data)) == 13


def test_second():
    assert second(io.StringIO(data)) == 1
    assert second(io.StringIO(data2)) == 36
