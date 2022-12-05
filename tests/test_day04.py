import io
from advent.days.day04 import Assignment, first, fully_contains, second
import pytest

data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
data_io = io.StringIO(data)


@pytest.mark.parametrize('a1, a2, expected', [
    ('2-8', '3-7', True),
    ('3-7', '2-8', True),
    ('6-6', '4-6', True),
    ('2-3', '4-5', False),
])
def test_fully_contains(a1, a2, expected):
    a1, a2 = Assignment.from_str(a1), Assignment.from_str(a2)
    assert fully_contains(a1, a2) == expected


def test_first():
    assert first(io.StringIO(data)) == 2


def test_second():
    assert second(io.StringIO(data)) == 4
