from typing import TextIO


def first(input: TextIO) -> int:
    elves = [[int(n) for n in e.split()] for e in input.read().split('\n\n')]
    max_cal = max(sum(e) for e in elves)
    return max_cal


def second(input: TextIO) -> int:
    elves = [[int(n) for n in e.split()] for e in input.read().split('\n\n')]
    calories_per_elf = sorted([sum(e) for e in elves], reverse=True)
    return sum(calories_per_elf[:3])
