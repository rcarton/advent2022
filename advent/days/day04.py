from dataclasses import dataclass
from typing import TextIO


@dataclass
class Assignment:
    start: int
    end: int

    @classmethod
    def from_str(cls, s):
        return Assignment(*map(int, s.split('-')))


def fully_contains(a1: Assignment, a2: Assignment) -> bool:
    return (a1.start <= a2.start and a1.end >= a2.end) or (a2.start <= a1.start and a2.end >= a1.end)


def overlaps(a1: Assignment, a2: Assignment) -> bool:
    return fully_contains(a1, a2) \
           or (a1.start <= a2.start <= a1.end) \
           or (a2.start <= a1.start <= a2.end)


def first(input: TextIO) -> int:
    pairs_str = [l.split(',') for l in input.read().split('\n') if l]
    assignment_pairs = [(Assignment.from_str(a1), Assignment.from_str(a2)) for a1, a2 in pairs_str]
    return sum(map(lambda x: int(fully_contains(*x)), assignment_pairs))


def second(input: TextIO) -> int:
    pairs_str = [l.split(',') for l in input.read().split('\n') if l]
    assignment_pairs = [(Assignment.from_str(a1), Assignment.from_str(a2)) for a1, a2 in pairs_str]
    return sum(map(lambda x: int(overlaps(*x)), assignment_pairs))
