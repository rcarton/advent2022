import io
import pytest

from advent.days.day06 import first, get_first_marker_index, second

data = """zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
"""
data_io = io.StringIO(data)


@pytest.mark.parametrize('buf, expected', [
    ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5),
    ('nppdvjthqldpwncqszvftbrmjlhg', 6),
    ('abcde', 4),
    ('bbcde', 5),
])
def test_get_first_marker_index(buf: str, expected: int):
    assert get_first_marker_index(buf) == expected


def test_first():
    assert first(io.StringIO(data)) == 11


def test_second():
    assert second(io.StringIO(data)) == 26
