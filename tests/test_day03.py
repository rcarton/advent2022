import io

import pytest as pytest

from advent.days.day03 import first, prio, second

data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
data_io = io.StringIO(data)


@pytest.mark.parametrize('c, expected', [
    ('a', 1),
    ('b', 2),
    ('z', 26),
    ('A', 27),
    ('Z', 52),
])
def test_prio(c, expected):
    assert prio(c) == expected


def test_first():
    assert first(io.StringIO(data)) == 157


def test_second():
    assert second(io.StringIO(data)) == 70
