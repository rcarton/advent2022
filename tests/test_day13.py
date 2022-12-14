import io
import pytest

from advent.days.day13 import first, merge_sort_in_place, second

data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
data_io = io.StringIO(data)


@pytest.mark.parametrize('nums, expected', [
    ([2, 1, 3], [1, 2, 3])
])
def test_merge_sort_in_place(nums, expected):
    merge_sort_in_place(nums)
    assert nums == expected


def test_first():
    assert first(io.StringIO(data)) == 13


def test_second():
    assert second(io.StringIO(data)) == 140
