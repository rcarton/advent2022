import io
import pytest

from advent.days.day08 import first, scenic_score_direction, second

data = """30373
25512
65332
33549
35390
"""
data_io = io.StringIO(data)


@pytest.mark.parametrize('tree, other_trees, expected', [
    (5, [3, 5, 3], 2),
    (5, [], 0),
    (5, [3], 1),
    (5, [5], 1),
])
def test_scenic_score_direction(tree, other_trees, expected):
    assert scenic_score_direction(tree, other_trees) == expected


def test_first():
    assert first(io.StringIO(data)) == 21


def test_second():
    assert second(io.StringIO(data)) == 8
