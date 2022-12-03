import io

from advent.days.day02 import first, second

data = """A Y
B X
C Z"""


def test_first():
    assert first(io.StringIO(data)) == 15


def test_second():
    assert second(io.StringIO(data)) == 12
