import itertools as it
from collections import deque
from typing import Iterable, Iterator, TextIO, Tuple, TypeVar


def get_first_marker_index(buf: str, count=4) -> int:
    for i in range(count, len(buf) + 1):
        if len(set(buf[i - count:i])) == count:
            return i
    raise Exception('No marker found')


def first(input: TextIO) -> int:
    return get_first_marker_index(input.read().replace('\n', ''))


def second(input: TextIO) -> int:
    return get_first_marker_index(input.read().replace('\n', ''), 14)
