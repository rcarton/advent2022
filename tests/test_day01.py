import io

from advent.days.day01 import first, second

data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


def test_first():
    data_io = io.StringIO(data)
    assert first(data_io) == 24000


def test_second():
    assert second(io.StringIO(data)) == 45000
