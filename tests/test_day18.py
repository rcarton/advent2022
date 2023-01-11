import io

from advent.days.day18 import first, second

data = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""
data_io = io.StringIO(data)


def test_first():
    assert first(io.StringIO(data)) == 64


def test_second():
    assert second(io.StringIO(data)) == 58
