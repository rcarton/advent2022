from enum import IntEnum
from typing import TextIO


class Play(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


MAPPING = {
    'A': Play.ROCK,
    'B': Play.PAPER,
    'C': Play.SCISSORS,
    'X': Play.ROCK,
    'Y': Play.PAPER,
    'Z': Play.SCISSORS,
}

MAPPING_RESULT = {
    'X': -1,  # Loss
    'Y': 0,  # Draw
    'Z': 1,  # Win
}


def figure_out_play(p: Play, result: str) -> Play:
    new_p = (p - 1 + MAPPING_RESULT[result]) % 3 + 1
    return Play(new_p)


def score(p1: Play, p2: Play) -> int:
    """
    p1 is me
    """

    # Draw
    if p1 == p2:
        return p1 + 3

    if p1 - (p2 % 3) == 1:
        return p1 + 6

    return p1


def first(input: TextIO) -> int:
    hands = [(MAPPING[p2], MAPPING[p1]) for p1, p2 in [h.split(' ') for h in input.read().split('\n') if h]]
    return sum(score(*hand) for hand in hands)


def second(input: TextIO) -> int:
    hands = [(figure_out_play(MAPPING[p1], result), MAPPING[p1]) for p1, result in
             [h.split(' ') for h in input.read().split('\n') if h]]
    return sum(score(*hand) for hand in hands)
