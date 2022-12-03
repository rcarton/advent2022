from functools import reduce
from typing import TextIO

from advent.utils import chunk


def prio(c: str) -> int:
    o = ord(c)
    return o - ord('a') + 1 if o > ord('Z') else o - ord('A') + 27


def first(input: TextIO) -> int:
    lines = [l for l in input.read().split('\n') if l]
    rucksacks = [(set(l[:len(l) // 2]), set(l[len(l) // 2:])) for l in lines]
    common = [a & b for a, b in rucksacks]
    return sum(sum(prio(c) for c in rucksack) for rucksack in common)


def second(input: TextIO) -> int:
    lines = [l for l in input.read().split('\n') if l]
    groups = chunk(lines, 3)
    badges = [reduce(lambda a, b: a & set(b) if a else set(b), g, set()) for g in groups]
    return sum(sum(prio(c) for c in b) for b in badges)
